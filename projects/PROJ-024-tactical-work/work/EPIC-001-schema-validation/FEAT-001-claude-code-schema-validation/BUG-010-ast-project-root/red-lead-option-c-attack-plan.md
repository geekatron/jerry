# red-lead Option C Re-Check Attack Plan — BUG-010 `jerry ast` Containment (Trusted Roots)

> **Engagement:** RED-BUG010 (re-check pass 2) — white-box source-code security re-assessment of the `jerry ast` path-containment REDESIGN from always-auto-widen to **Option C (user-declared trusted roots)**.
> **Agent:** red-lead (Engagement Lead and Scope Authority) — Step 1 of `/red-team`. MANDATORY FIRST agent; red-vuln executes against this plan.
> **Deliverable type:** Updated scope confirmation + threat model delta + ENUMERATED attack cases (AC-1..AC-21). **METHODOLOGY AND PLAN ONLY** — no exploit execution, no code modification by red-lead.
> **Target:** Branch `fix/BUG-010-ast-project-root` @ `da34a8b8` (Option C). Changed files: `src/interface/cli/containment_policy.py` (NEW, pure policy), `src/interface/cli/project_root.py` (I/O boundary + config read), `src/interface/cli/ast_commands.py` (enforcement + `ast_modify` write path), plus `parser.py`/`main.py`/`adapter.py` CLI wiring.
> **Authorization:** Repo owner (geekatron), PR #341 review — authorized internal defensive review of Jerry's own CLI. No live systems, no network. Source-level adversarial analysis feeding red-vuln.
> **Methodology:** PTES Pre-Engagement + NIST SP 800-115 §3 (Planning) + OSSTMM §III, applied to a white-box diff review.

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | What changed, re-check thesis, headline residual risks |
| [L1 Scope Delta and Rules of Engagement](#l1-scope-delta-and-rules-of-engagement) | In/out of scope, RoE (unchanged), targets |
| [L1 Threat Model of the Option C Surface](#l1-threat-model-of-the-option-c-surface) | New trust boundary, attack-surface delta vs. prior pass |
| [L1 Attack Cases — Group A: Confirm Prior Criticals Dissolved](#l1-attack-cases--group-a-confirm-prior-criticals-dissolved-c1c6) | AC-1..AC-6 (C1–C6 re-verification) |
| [L1 Attack Cases — Group B: New Option C Surface](#l1-attack-cases--group-b-new-option-c-surface) | AC-7..AC-18 (trusted_roots, env precedence, resolution, is_relative_to) |
| [L1 Attack Cases — Group C: Cross-Platform Correctness](#l1-attack-cases--group-c-cross-platform-correctness) | AC-19..AC-21 (Windows/macOS/POSIX) |
| [L1 Severity Rubric](#l1-severity-rubric) | Scoring model red-vuln applies (unchanged) |
| [L2 Strategic Implications](#l2-strategic-implications) | Most-likely-finding call, coverage-gap guidance |
| [Agent Authorizations](#agent-authorizations) | Which /red-team agents may act |
| [Constitutional Compliance](#constitutional-compliance) | P-001/P-002/P-020/P-022 attestation |

---

## L0 Executive Summary

**What changed since the prior pass.** The prior engagement (RED-BUG010 pass 1) assessed an *always-widen* design whose default allowed set was `{project_root, tempfile.gettempdir(), /tmp}`. It produced two CONFIRMED findings — **H-01** (multi-user temp read/write, no ownership gate) and **H-02** (broad-root warning coverage gap) — plus a separate C4 `/adversary` tournament that surfaced six Critical clusters **C1–C6**. The design was then **replaced wholesale by Option C**: containment defaults to the project root plus zero-or-more *user-declared* `ast.trusted_roots` config entries. Temp is never auto-trusted. The temp-ownership gate was removed entirely. `--root` remains an exclusive single-root override.

**Re-check thesis (what red-vuln must prove, not assume).** Option C claims to *dissolve* most of C1–C6 by construction rather than patch them. That claim is plausible from the code but MUST be positively verified against the shipped `da34a8b8` source, because a redesign can silently reintroduce an old class through a new mechanism. Two things are simultaneously true and must both be tested: (1) the old attack classes have no surface left, and (2) the new `ast.trusted_roots` mechanism does not open a *new* silent-widening path.

**Headline residual-risk hypotheses (pre-execution — these are directions to test, not findings):**

1. **Empty / whitespace `ast.trusted_roots` entries resolve to cwd (AC-11).** `_load_trusted_roots()` returns raw strings; `get_containment_roots()` does `Path(entry).resolve()` per entry (`project_root.py:174`). `Path("").resolve()` returns the current working directory. An empty-string entry (from `JERRY_AST__TRUSTED_ROOTS=""`, or a stray `""` in a TOML array) would silently add **cwd** as a `configured` trusted root — a widening the user never intended, with no broad-root warning unless cwd happens to be broad. This is the highest-value new-surface hypothesis.
2. **Relative `trusted_roots` entries resolve against cwd (AC-10).** Documented as a "foot-gun" in the code itself (`project_root.py:110-112`). A relative entry (`"scratch"`, `"../shared"`) resolves against wherever the process was launched, so the trusted set is *invocation-directory dependent* — a caller lured into running `jerry ast` from an attacker-influenced cwd gets a different (possibly wider, possibly parent-escaping via `..`) trust set.
3. **Broad configured root is allowed-with-warning, not blocked (AC-16).** DD-1 extends the broad-root warning to `configured` roots, but a broad `ast.trusted_roots` entry (`/`, `/Users`, `$HOME`) still *proceeds* — containment is effectively disabled, only now via config rather than `--root`. Confirm the warning fires for the `configured` classification (not just `explicit`) and that broadness detection is complete (ancestor-of-home, drive roots, Windows `C:\Users`).

**Expected-SAFE (positive-assurance) directions.** C1 (index trust), C3/C4 (ownership fail-open / same-UID), C5 (`TMPDIR` poisoning), C2 (read/write TOCTOU divergence), and `is_relative_to` component-wise matching all *appear* dissolved or correct in `da34a8b8`. red-vuln must demonstrate the invariant holds, per the owner's explicit request for a red-team pass — not infer it from reading.

---

## L1 Scope Delta and Rules of Engagement

### Authorized targets (allowlist — everything else OUT OF SCOPE)

| # | Target | Type |
|---|--------|------|
| T-1 | `src/interface/cli/containment_policy.py` | NEW pure policy: `ContainmentRoot`, `resolve_allowed_roots`, `_is_broad_containment_root` |
| T-2 | `src/interface/cli/project_root.py` | I/O boundary: `get_project_root`, `build_layered_config_adapter`, `_load_trusted_roots`, `get_containment_roots` |
| T-3 | `src/interface/cli/ast_commands.py` | Enforcement: `_check_path_containment`, `_note_if_configured_root_match`, `_read_file`, `ast_modify` write path |
| T-4 | `src/interface/cli/parser.py`, `main.py`, `adapter.py` | `--root`/`--quiet` plumbing, `ast.trusted_roots` defaults registration |
| T-5 | `src/infrastructure/adapters/configuration/layered_config_adapter.py`, `env_config_adapter.py` | Config precedence + env-key mapping (`get_list`, `_env_to_config_key`) — as they feed the trust decision |
| T-6 | Associated tests as *evidence of coverage*, not attack targets | Test-adequacy review |

### Rules of Engagement (unchanged from pass 1 — restated for the re-check)

- White-box, source-available, read-only against source. Dynamic tests permitted ONLY in-process (pytest-style) or via `jerry ast` against files the assessor creates in a **disposable, assessor-owned sandbox** (`mkdtemp`). No network.
- NEVER point a write-capable test (`ast_modify`) at any real user/system file. Stand-in "victim"/"secret" fixtures contain **synthetic data only**; never read or echo a real credential or any part of one.
- No modification of production source, tests, or the worktracker by assessment agents. Findings are reported, not patched (P-020).
- `JERRY_DISABLE_PATH_CONTAINMENT=1` is an intentional, documented test-only bypass — note its existence but do NOT treat "containment can be disabled by an env var the user sets themselves" as a finding (user discretion by design, same class as `--root`).
- Emergency stop: if any test would touch a path outside the sandbox, HALT and model it instead. red-lead is circuit-breaker authority for any `SCOPE_REVIEW_REQUIRED`.

### Out of scope

Live hosts/services/network; the M-05 1 MB size cap logic itself (unchanged); the domain/markdown-AST parsers except where a containment path reaches them; persistence/exfil/C2/social engineering (none authorized).

---

## L1 Threat Model of the Option C Surface

### Trust boundary: prior pass vs. this pass

```
PASS 1 (always-widen — now DELETED):
  allowed(default) = [ project_root ] ∪ [ gettempdir() ] ∪ [ /tmp ]      # auto, no user action
  attacker inputs  = file_path (+ --root)
  key risk         = world-writable multi-tenant temp in the DEFAULT set, no ownership gate

PASS 2 (Option C — under test @ da34a8b8):
  allowed(default) = [ project_root ] ∪ [ resolve(e) for e in ast.trusted_roots ]   # user-declared only
  allowed(--root X)= [ resolve(X) ]                                                  # exclusive
  attacker inputs  = file_path, --root, AND the ast.trusted_roots config channel
                     (env JERRY_AST__TRUSTED_ROOTS  >  project .jerry/config.toml  >  root .jerry/config.toml  >  [])
  key risk shift   = from "auto-trusted temp" to "silent widening via the config channel"
                     (empty/relative/symlinked/broad entries; env-key mis-mapping; cwd-relative resolution)
```

### Structural observations that shape the cases

1. **Containment is evaluated on fully-resolved paths on both sides.** File: `resolved = Path(file_path).resolve()` (`ast_commands.py:248`) + `realpath = os.path.realpath(file_path)` (`:253`). Roots: `Path(entry).resolve()` (`project_root.py:174`) and `Path(explicit_root).resolve()` (`:170`). Symlinks and `..` are dereferenced *before* comparison. This is what makes symlink-escape and traversal rejection sound — verify it still holds for the `configured` classification, not just project/explicit.
2. **Classification is structural, not positional.** `resolve_allowed_roots` labels each root `project`|`configured`|`explicit` by *origin* (`containment_policy.py:143-173`); the old `matched_root != allowed_roots[0]` index test is gone. The C1 attack class (smuggle trust via index-0) has no code to target — confirm by grep + behavior.
3. **The config channel is the new attacker-adjacent surface.** Anything that can influence `JERRY_AST__TRUSTED_ROOTS`, the project/root `.jerry/config.toml`, or the process cwd can influence the trusted set. Precedence and env-key mapping are load-bearing security logic now.
4. **`is_relative_to` is pathlib component-wise, not string-prefix.** `/a/bc`.is_relative_to(`/a/b`) is `False`. Confirm no sibling-prefix escape.

### CWE / ATT&CK framing (framing only — code review, not live attack)

| Surface | Primary CWE | Concern |
|---|---|---|
| `ast.trusted_roots` empty/relative entry → cwd | CWE-73 (External Control of Path), CWE-426 (Untrusted Search Path) | Silent widening to cwd / invocation-dir-dependent trust |
| Env-key mapping (`__` vs `_`), value parsing | CWE-20 (Improper Input Validation) | Mis-mapping either silently no-ops (safe) or silently widens (finding) |
| Configured root = symlink or contains `..` | CWE-59 (Link Resolution), CWE-22 (Traversal) | Root resolution must dereference safely |
| Broad configured root | CWE-1284 (incomplete allowlist) / advisory | Containment effectively disabled via config |
| `is_relative_to` sibling prefix | CWE-22 | Component-wise vs string-prefix |
| `ast_modify` read→write symlink swap | CWE-367 (TOCTOU) | Write-time recheck must re-resolve |
| Advisory note / `--quiet` | robustness | Must never suppress enforcement; never reach stdout |
| Windows path flavor | CWE-22 / CWE-59 | POSIX-only assumptions changing behavior |

---

## L1 Attack Cases — Group A: Confirm Prior Criticals Dissolved (C1–C6)

> Each case: **Precondition · Steps · Expected-if-secure · What-would-prove-a-finding.** red-vuln executes in-process/sandbox against the real `da34a8b8` functions. Cite exact line(s) as evidence (P-001).

### AC-1 — C1: No residual index/position-based trust in classification
- **Precondition:** Default set (no `--root`) with at least one `configured` root, so `allowed_roots` has ≥2 entries.
- **Steps:** (1) Static: grep `containment_policy.py` + `ast_commands.py` for `[0]`, `allowed_roots[`, `roots[`, and any "first entry is safe/project" assumption. (2) Behavioral: build `resolve_allowed_roots(project_root, [configured_A, configured_B], None)`; assert each returned `ContainmentRoot.classification` is by origin (`project` for index 0, `configured` for the rest) and that *reordering* the configured list does not change any entry's classification or trust treatment. (3) Construct a case where the **project root itself resolves inside a configured tree** and confirm it is still classified `"project"` (not silently reclassified) and that a configured root duplicating the project root is deduped keeping `"project"` (`containment_policy.py:152-172`).
- **Expected-if-secure:** Classification is purely origin-derived; no code path treats "index 0" as a trust signal; dedup keeps `project`. (red-lead pre-check: grep found only unrelated `events[0]`/error-tuple `[0]` in `adapter.py`/`main.py`, none in containment files.)
- **Proves a finding if:** Any trust/warning/ownership decision keys off array position; or reordering configured roots changes enforcement; or a configured root can displace/alias the project classification.

### AC-2 — C2: `ast_modify` read→write symlink swap caught by write-time re-resolution
- **Precondition:** A file inside an allowed root whose path is (or can become) a symlink; `_ENFORCE_PATH_CONTAINMENT` true (do NOT set `JERRY_DISABLE_PATH_CONTAINMENT`).
- **Steps:** (1) In sandbox, create `link.md` inside an allowed root pointing to an in-root target; run `ast_modify` read succeeds. (2) Simulate the swap: between read and write, repoint `link.md` to a target **outside all allowed roots**. Because the design calls `_check_path_containment(file_path, root, quiet=True)` at write time (`ast_commands.py:634-638`) — which re-runs `Path(file_path).resolve()` AND `os.path.realpath(file_path)` fresh — assert the write is **rejected** (exit 2, "escapes allowed containment roots at write time") and the original file is unmodified. (3) Variant: swap to a target inside a *different* allowed root; confirm no write-through to an unvalidated path — note that `target_path` is resolved at `:620` (before the recheck) while the recheck re-resolves at `:635`; confirm the actually-written path (`os.replace(temp, str(target_path))`, `:654`) is the read-time-validated resolved path and cannot land outside all roots.
- **Expected-if-secure:** Write-time recheck is the identical function as read time; a swap-to-outside is rejected; `os.replace` replaces the symlink itself (rename semantics), never writes through it; residual window is bounded by rename atomicity.
- **Proves a finding if:** Write proceeds after a swap-to-outside; or the written `target_path` (resolved at `:620`) can diverge from the rechecked path (`:635`) such that a write lands outside every allowed root; or any fallback non-`mkstemp` write path exists.

### AC-3 — C3/C4: Ownership/UID gate fully removed; no fail-open on a security decision
- **Precondition:** None (static + behavioral).
- **Steps:** (1) Grep `ast_commands.py`, `project_root.py`, `containment_policy.py` for `st_uid`, `geteuid`, `os.name`, `_check_temp_root_ownership`, `_is_temp_default_root_match` — expect **zero** matches (gate removed per DD-2). (2) Audit every `except` in the enforcement path and classify fail-open vs fail-closed on a *security* decision: `ast_commands.py:249` (resolve error → returns error = fail-closed ✓), `:278` (size stat error → returns error = fail-closed ✓). (3) In `containment_policy.py`, audit `:90` (`Path.home()` undeterminable → returns `False`) and `:105` (`relative_to` non-ancestor → returns `False`): confirm these govern only the **advisory `is_broad` warning**, never the allow/deny enforcement decision.
- **Expected-if-secure:** No ownership logic survives; every fail-open branch affects only advisory output, not enforcement; enforcement stat/resolve errors fail closed.
- **Proves a finding if:** Any surviving ownership/uid code path gates enforcement; or an `except ... : pass`/`return False`/`return None-error` on the enforcement (allow/deny) path lets a non-contained path through.

### AC-4 — C3 residual: broad-detection fail-open changes an *enforcement* outcome
- **Precondition:** Environment where `Path.home()` raises (`RuntimeError`/`OSError`) — e.g., unset `HOME`/`USERPROFILE`.
- **Steps:** Monkeypatch `Path.home` to raise; call `_is_broad_containment_root` on `/`, `/Users`, an ordinary dir. Then call `get_containment_roots` with a broad `configured` root under the same condition and assert the *containment allow/deny* result is unchanged (only the warning may be suppressed).
- **Expected-if-secure:** `Path.home()` failure suppresses only the ancestor-of-home *warning*; a filesystem/drive root is still flagged broad via `len(parts)<=1` (`:86`); enforcement is unaffected.
- **Proves a finding if:** A `Path.home()` failure changes which files are allowed (not just whether a warning prints).

### AC-5 — C5: No `tempfile`/`TMPDIR`/`/tmp` feeds the allowed-root set
- **Precondition:** Attacker-controlled `TMPDIR`/`TEMP`/`TMP` env; no `ast.trusted_roots` configured.
- **Steps:** (1) Grep `project_root.py` + `containment_policy.py` for `gettempdir`, `_HARDCODED_TMP`, `tempfile`, `TMPDIR` in the *allowed-roots computation* (expect matches only in docstrings/comments; the only live `tempfile` use is `mkstemp` write-staging in `ast_commands.py:644`). (2) Behavioral: set `TMPDIR=/attacker/dir`, call `get_containment_roots()` (no `--root`, no config) and assert the returned set is **exactly `[project_root]`** — no temp-derived entry. (3) Place a synthetic file under `gettempdir()` and assert `_check_path_containment` **rejects** it by default.
- **Expected-if-secure:** `TMPDIR`/`TEMP`/`TMP` have zero effect on containment; default set is project-root-only.
- **Proves a finding if:** Any temp-derived path appears in the allowed set, or a `gettempdir()` file is allowed by default.

### AC-6 — C6: `--quiet` never suppresses enforcement; no advisory note reaches stdout
- **Precondition:** A `configured`-root match (fires the R-4 note) and a broad `configured`/`explicit` root (fires the R-3 warning).
- **Steps:** (1) Run each `ast_*` command with `--quiet` and confirm the allow/deny outcome is **identical** to non-quiet (quiet only guards `if not quiet:` print blocks in `project_root.py:177` and `_note_if_configured_root_match` in `ast_commands.py:200`; roots returned are quiet-independent). (2) Capture streams: assert the R-3 warning and R-4 note appear on **stderr only**, never stdout, so `jerry ast ... | jq` stays valid. (3) Confirm `ast_modify`'s write-time internal recheck hard-codes `quiet=True` (`:635`) yet still **enforces** (returns 2 on violation) — quiet ≠ disabled. (4) Note (robustness, not a Group-C escape): enforcement *rejection* messages use bare `print(f"Error: ...")` → **stdout** (`ast_commands.py:311, 637`); flag whether error-on-stdout could confuse a JSON consumer, but this is pre-existing and replaces (not corrupts) the payload.
- **Expected-if-secure:** `--quiet` suppresses only advisory stderr text; enforcement is unconditional; no advisory note is ever written to stdout.
- **Proves a finding if:** `--quiet` (or the write-time `quiet=True`) changes any allow/deny outcome, or any advisory note/warning is emitted to stdout.

---

## L1 Attack Cases — Group B: New Option C Surface

### AC-7 — `ast.trusted_roots` precedence order is exactly env > project > root > default
- **Precondition:** Configure `ast.trusted_roots` at multiple layers with distinguishable values.
- **Steps:** Set root `.jerry/config.toml` → `[R]`; project `projects/{JERRY_PROJECT}/.jerry/config.toml` → `[P]`; env `JERRY_AST__TRUSTED_ROOTS` → `["E"]`. Call `_load_trusted_roots()`/`get_containment_roots()` and assert the winning layer at each combination. Confirm project config path derives from `JERRY_PROJECT` (`project_root.py:86-90`) and the anchor is `get_project_root().resolve()` (`:85`), NOT the Jerry install tree.
- **Expected-if-secure:** Highest present layer wins: env > project > root > `[]`. Missing `JERRY_PROJECT` → no project layer, falls through to root/default.
- **Proves a finding if:** A lower layer overrides a higher one; or a layer file outside the user's project (e.g., Jerry install dir) is read; or precedence differs from the documented 4-layer model in a way that widens trust.

### AC-8 — Env-key mapping: single-underscore mis-form is a safe no-op, not a silent widen
- **Precondition:** None.
- **Steps:** (1) Set `JERRY_AST_TRUSTED_ROOTS` (SINGLE underscore) `=["/attacker"]`; assert it does NOT enter the trusted set. Root cause to confirm: `_env_to_config_key` does `key.lower().replace("__", ".")` (`env_config_adapter.py:82`), so `AST_TRUSTED_ROOTS` → `ast_trusted_roots` (no dot) which never matches the dotted lookup `ast.trusted_roots`. (2) Confirm the correct double-underscore form `JERRY_AST__TRUSTED_ROOTS` → `ast.trusted_roots` DOES apply. (3) Over-underscored `JERRY_AST__TRUSTED__ROOTS` → `ast.trusted.roots` (no match) → safe no-op.
- **Expected-if-secure:** Only the exact `JERRY_AST__TRUSTED_ROOTS` form takes effect; every mis-form is silently ignored (fails safe, does not widen).
- **Proves a finding if:** Any mis-form *widens* the trusted set, or the correct form is silently dropped (availability regression, lower severity but worth noting).

### AC-9 — Env value parsing: scalar/CSV/JSON coercion cannot inject an unintended root
- **Precondition:** None.
- **Steps:** Exercise `JERRY_AST__TRUSTED_ROOTS` as: JSON array `["/a","/b"]`; bare CSV `/a,/b`; single scalar `/a`; a value containing a comma inside a path. Trace through `EnvConfigAdapter._parse_value` (`:98-149`) and `get_list` (`:214-229`): scalar → `[value]`; CSV (unquoted) → split on `,`; JSON → `json.loads`. Assert the resolved root set matches intent and that a path legitimately containing `,` is mangled by CSV-splitting (document as a correctness/foot-gun, not necessarily a security escape).
- **Expected-if-secure:** Parsing yields exactly the declared paths; no extra root is synthesized.
- **Proves a finding if:** A crafted value yields a broader set than declared (e.g., a stray element resolving to `/` or cwd) with no warning.

### AC-10 — Relative `trusted_roots` entry resolves against cwd (invocation-dir-dependent trust)
- **Precondition:** `ast.trusted_roots = ["scratch"]` or `["../shared"]` (relative); process launched from an attacker-influenceable cwd.
- **Steps:** Set a relative entry; from cwd `/A/B` call `get_containment_roots()` and assert the configured root resolves to `/A/B/scratch` (or `/A/shared` for `..`) via `Path(entry).resolve()` (`project_root.py:174`). Change cwd to `/X/Y` and re-call; assert the trusted root *moves* with cwd. Test a `..`-laden entry that resolves to a parent/sibling of the project.
- **Expected-if-secure:** Behavior is as documented (relative resolves against cwd — `project_root.py:110-112` calls it a foot-gun) and is at worst a documented usability hazard, not an escape beyond user intent.
- **Proves a finding if:** A relative entry can be steered (via cwd) to a location the user did not intend to trust *without any signal*, especially one that escapes upward via `..` into a broad or multi-user parent — recommend rejecting/normalizing relative entries or warning on them.

### AC-11 — Empty / whitespace `trusted_roots` entry silently resolves to cwd  **(highest-value new-surface case)**
- **Precondition:** An empty-string or whitespace entry reaches the list — via `JERRY_AST__TRUSTED_ROOTS=""`, a trailing comma in CSV (`"/a,"` → `["/a",""]`), or a stray `""` in a TOML array.
- **Steps:** (1) `JERRY_AST__TRUSTED_ROOTS=""` → `_parse_value("")` returns `""` → `get_list` wraps to `[""]` → `_load_trusted_roots` yields `[""]` → `Path("").resolve()` returns **cwd**. Assert whether cwd is thereby added as a `configured` root. (2) CSV trailing comma `"/a,"` and whitespace `" "` entries: trace whether they survive to `Path(...).resolve()` and what they resolve to. (3) Assess: if cwd == project_root the effect is nil, but if `CLAUDE_PROJECT_DIR` points elsewhere (cwd ≠ project root), an empty entry silently trusts cwd with NO broad-root warning (cwd is rarely broad).
- **Expected-if-secure:** Empty/whitespace entries are rejected or ignored before resolution; they never inject cwd into the trusted set.
- **Proves a finding if:** An empty/whitespace/degenerate entry adds cwd (or any unintended directory) to the trusted set silently. **red-lead assessment: likely a real finding — the code does not filter falsy entries before `Path(entry).resolve()`.** Severity LOW–MEDIUM (requires the config channel + cwd ≠ project root), +1 if reachable via `ast_modify`.

### AC-12 — Configured root that is a symlink resolves safely (no additive escape)
- **Precondition:** `ast.trusted_roots = ["/sandbox/link_root"]` where `link_root -> /sandbox/real_root` (or `-> /`).
- **Steps:** Configure a symlinked directory as a trusted root; assert `Path(entry).resolve()` (`:174`) dereferences it to the real target, and containment then compares files against the *resolved* target — not the symlink path. Confirm a file under the real target is allowed and a file outside it is rejected. If `link_root -> /`, confirm the resolved root is `/` and the broad-root warning fires (AC-16 linkage).
- **Expected-if-secure:** The root is fully resolved before comparison; no double-trust of both the symlink path and its target; broad targets warn.
- **Proves a finding if:** Both the symlink path and its resolved target are trusted (widening), or a symlinked root escapes broad-root detection.

### AC-13 — Configured root containing `..` is normalized before trust
- **Precondition:** `ast.trusted_roots = ["/sandbox/a/../.."]` (resolves to `/`) or `["/proj/sub/../../elsewhere"]`.
- **Steps:** Configure a `..`-laden entry; assert `Path(entry).resolve()` collapses it to the true target, and broad-root detection sees the *collapsed* path (so `/sandbox/a/../..` → `/` fires the warning). Confirm containment uses the collapsed root.
- **Expected-if-secure:** `..` is fully collapsed by `resolve()` before both the broad check and containment; no lexical-vs-real mismatch.
- **Proves a finding if:** Broadness or containment is computed on the un-normalized string while trust is granted on a different resolved path (lexical/real divergence).

### AC-14 — `is_relative_to` is component-wise, not string-prefix (sibling escape)
- **Precondition:** Project root `/a/b`; a sibling directory `/a/bc` outside it.
- **Steps:** With allowed root `/a/b`, check a file at `/a/bc/secret.md`. Assert `resolved.is_relative_to(Path("/a/b"))` is **False** (`ast_commands.py:257`) → rejected. Repeat for a configured root `/a/b` vs file `/a/b-sibling/...`. Repeat the symlink M-10 branch (`:266`) with the same sibling shape.
- **Expected-if-secure:** Component-wise matching rejects sibling-prefix paths; `/a/bc` is not "inside" `/a/b`.
- **Proves a finding if:** Any containment comparison uses string `startswith`/prefix logic that admits `/a/bc` under `/a/b`.

### AC-15 — Project root resolving inside a configured (or temp) tree does not re-open C1
- **Precondition:** `CLAUDE_PROJECT_DIR` set to a directory that itself lives under a configured trusted root (or under `gettempdir()`).
- **Steps:** Arrange project root nested inside a configured root; call `get_containment_roots()`; assert the project entry stays classified `"project"` (`containment_policy.py:154-159`), the configured entry is deduped if identical, and no ownership/index logic is triggered by the nesting. Confirm a file in the project is allowed as `project` (no R-4 note), and a file only under the configured tree gets the R-4 note.
- **Expected-if-secure:** Nesting is benign; classification remains origin-based; no C1-style positional trust emerges from the overlap.
- **Proves a finding if:** Nesting causes a misclassification, a suppressed warning that should fire, or a positional trust decision.

### AC-16 — Broad configured root: warning fires for `configured`, and broadness detection is complete
- **Precondition:** `ast.trusted_roots` set to each of: `/`, `$HOME`, `/home`, `/Users`, `$HOME`'s parent, a drive root.
- **Steps:** For each, call `get_containment_roots()` and capture stderr. Assert the **`configured`-classification** warning fires (`project_root.py:189-197`) — distinct wording from the `explicit` warning. Verify `_is_broad_containment_root` (`containment_policy.py:53-107`) flags: filesystem/drive root (`len(parts)<=1`), exact home, and **ancestor-of-home** (`/home`, `/Users`, `C:\Users`, home's parent) via `home.relative_to(resolved)`. Confirm the invocation still **proceeds** (broad root is allowed-with-warning, DD-1 accepted policy).
- **Expected-if-secure:** Every broad shape warns under the `configured` classification; enforcement proceeds (accepted). This is where the prior H-02 fix landed — confirm it is present and applied to configured roots, not only `--root`.
- **Proves a finding if:** A broad `configured` root proceeds with NO warning (the exact H-02 gap, now in the config channel), or the ancestor-of-home logic misses a known multi-user parent.

### AC-17 — `--root` exclusivity cannot be combined with configured roots to widen
- **Precondition:** Both `--root X` supplied AND `ast.trusted_roots` configured.
- **Steps:** Call `get_containment_roots(explicit_root=X)` with configured roots present in config; assert the returned set is **exactly `[X as "explicit"]`** — configured roots are passed as `[]` to `resolve_allowed_roots` when explicit is set (`project_root.py:169-171`, `containment_policy.py:143-150`). Assert a file inside a configured (non-X) root is **rejected** under `--root X`, and a project-root file is rejected too (pure exclusivity).
- **Expected-if-secure:** `--root` is a true exclusive override; configured roots and project root are entirely ignored while it is set.
- **Proves a finding if:** Any configured root (or the project root) remains admissible alongside `--root`, i.e., `--root` becomes additive rather than exclusive.

### AC-18 — Config read cannot be steered to a file outside the user's project
- **Precondition:** Adversary influence over `CLAUDE_PROJECT_DIR` / `JERRY_PROJECT` / cwd.
- **Steps:** Confirm `build_layered_config_adapter` anchors both `root_config_path` and `project_config_path` to `get_project_root().resolve()` (`project_root.py:85, 90, 94-96`). Test: does an absolute or `..`-laden `JERRY_PROJECT` value cause the project config path to escape the project tree (`root / "projects" / jerry_project / ".jerry" / "config.toml"`, `:90`)? A `JERRY_PROJECT="../../etc"` would build `root/projects/../../etc/.jerry/config.toml`.
- **Expected-if-secure:** Config files are only ever read from within the resolved project tree; `JERRY_PROJECT` cannot traverse to arbitrary config locations, or if it can, that is an accepted user-controlled value with no privilege boundary crossed.
- **Proves a finding if:** A crafted `JERRY_PROJECT`/`CLAUDE_PROJECT_DIR` causes `ast.trusted_roots` to be sourced from an attacker-chosen config file outside the intended project, silently widening trust.

---

## L1 Attack Cases — Group C: Cross-Platform Correctness

> Jerry targets macOS, Linux, Windows. CI runs `windows-latest`. No live Windows host is in scope — execute as pure `PurePath`/`PureWindowsPath` reasoning plus behavioral tests where the host flavor allows.

### AC-19 — Windows broad-root detection completeness (drive root, `C:\Users`, UNC)
- **Precondition:** `PureWindowsPath` reasoning against `_is_broad_containment_root`.
- **Steps:** Evaluate `PureWindowsPath("C:\\")` (parts len 1 → broad ✓), `PureWindowsPath("C:\\Users")` (2 parts; must be caught by ancestor-of-home once `Path.home()` is `C:\Users\<u>`), `PureWindowsPath("\\\\host\\share")` (single anchor → broad ✓), `PureWindowsPath("\\\\host\\share\\sub")` (2 parts, not ancestor of home → **not** flagged). Note the ancestor-of-home check relies on `Path.home()` being the native flavor; the `TypeError` guard (`:105`) covers mixed-flavor comparisons.
- **Expected-if-secure:** Drive root and UNC share root warn; `C:\Users` warns via ancestor-of-home. UNC-subpath (`\\host\share\sub`) not flagged is the same advisory-only residual class as the prior H-08 note (document, do not escalate).
- **Proves a finding if:** `C:\Users` (a genuine multi-user parent) fails to warn on Windows, or any enforcement (not just warning) behaves differently on Windows path flavor.

### AC-20 — Case-sensitivity of `is_relative_to` on macOS/Windows (case-insensitive filesystems)
- **Precondition:** Configured/project root `/Users/Me/Trusted`; file accessed as `/users/me/trusted/x.md` (case variant) on a case-insensitive FS.
- **Steps:** Reason about + (where host allows) test whether `Path.resolve()` canonicalizes case to the on-disk form on macOS/Windows, and whether `is_relative_to` (case-sensitive in pathlib) then rejects a legitimately-in-root file whose case differs. Determine direction: case mismatch makes containment MORE restrictive (fail-closed) — confirm it cannot be used to *bypass* (a file outside the root cannot be admitted by case games), only to over-reject.
- **Expected-if-secure:** Case handling is fail-closed (over-rejects at worst); `resolve()` canonicalization keeps root and file consistent; no case trick admits an out-of-root path.
- **Proves a finding if:** A case-variant path is admitted *under* a root it does not truly belong to, or resolution inconsistency between root and file lets an outside path match.

### AC-21 — POSIX-only assumptions in resolution / realpath / os.replace on Windows
- **Precondition:** Review of `ast_commands.py` write + symlink path for POSIX-specific behavior.
- **Steps:** Audit: `os.path.realpath` (`:253`) symlink semantics on Windows (reparse points/junctions resolve differently pre/post Python 3.8 — confirm the M-10 secondary check still holds), `os.replace` (`:654`) atomic-rename guarantees on Windows (replacing an open/locked target can raise `PermissionError`, an `OSError` subclass caught at `:656` → fail-closed), and `tempfile.mkstemp` mode `0o600` semantics on Windows (POSIX perms are a no-op; Windows relies on per-user `%TEMP`/ACLs). Confirm none of these *silently* changes the allow/deny decision — only availability/robustness.
- **Expected-if-secure:** All platform differences are availability/robustness (fail-closed), never a containment relaxation.
- **Proves a finding if:** A Windows-specific resolution/realpath/junction behavior lets a write or read escape the allowed roots that would be rejected on POSIX.

---

## L1 Severity Rubric

(Unchanged from pass 1 — restated so red-vuln scores consistently.)

| Severity | Definition (this engagement) |
|----------|------------------------------|
| **CRITICAL** | Containment fully defeated with attacker-controlled input under DEFAULT config (no `--root`, no config channel, no env bypass) on a single-user host. |
| **HIGH** | Containment escape or unauthorized cross-tenant access reachable under default config on a shared/CI host, OR any write outside intended roots. |
| **MEDIUM** | Access broadening requiring a specific-but-realistic condition (config-channel influence, cwd ≠ project root, multi-user), OR a narrowly-safe invariant. |
| **LOW** | Weakness in an advisory control (warning/transparency), robustness/coverage gap, or theoretical race with strong OS compensating controls. |
| **INFO / ACCEPTED** | Behaves as owner explicitly accepted (declared trust proceeds; `--root` discretion; `JERRY_DISABLE_PATH_CONTAINMENT`). |

**Modifiers:** +1 if reachable via `ast_modify` (write). +1 if reachable with no `--root` and no explicit config action (pure default). −1 if a standard OS control independently blocks exploitation. State the assumed deployment model (single-user laptop vs shared/CI host) explicitly for any multi-tenant-dependent case.

---

## L2 Strategic Implications

**Most-likely-finding call (explicit, per owner request).** Option C dissolves the pass-1 headline (H-01 multi-user temp) *by construction* — temp is no longer in the default set, and the ownership gate that C3/C4 attacked is gone. The residual risk has **migrated from the OS-temp channel to the config channel.** Of the 21 cases, the ones with concrete, code-grounded gaps rather than "verify the invariant holds" are:

1. **AC-11 (empty/whitespace `trusted_roots` → cwd)** — the code applies `Path(entry).resolve()` to every raw string without filtering falsy/degenerate entries; `Path("").resolve()` is cwd. Most likely to reproduce; LOW–MEDIUM depending on `CLAUDE_PROJECT_DIR` ≠ cwd and write-reachability.
2. **AC-10 (relative entries → cwd-dependent trust)** — self-documented foot-gun; deterministic; recommend normalize-or-warn.
3. **AC-16 residual / AC-19 (broad-root completeness on the configured channel and on Windows `C:\Users`)** — the H-02 ancestor-of-home fix appears present in `containment_policy.py`; the re-check must confirm it is (a) actually wired to the `configured` classification, not just `explicit`, and (b) portable to `PureWindowsPath`.

Everything in Group A (C1, C2, C3/C4, C5, C6) and AC-12/13/14/15/17 is expected **SAFE / positive-assurance**: classification is structural, the write-time recheck is the same function call, the ownership gate and temp seams are deleted, `resolve()` normalizes symlinks and `..` before comparison, `is_relative_to` is component-wise, and `--root` is exclusive. Their value is *proving the redesign did not silently reintroduce an old class* — exactly what a re-check pass is for.

**The one systemic recommendation to carry into red-vuln's report.** The trust decision is now only as safe as the *input hygiene* on the config channel. The prior design's risk was "trusts location not ownership"; this design's risk is "trusts declared strings without normalization." The highest-leverage hardening is to **filter and normalize `ast.trusted_roots` entries before `resolve()`**: drop empty/whitespace entries, reject or warn on relative entries, and apply the broad-root warning (already computed per root) to every `configured` entry. This closes AC-10/AC-11/AC-16 with one input-sanitization pass and preserves the owner's declared-trust use case exactly.

**Coverage-gap guidance for downstream agents.** The eng-lead TDD list (Section 4 of `eng-lead-option-c-plan.md`) covers precedence, dedup, broad-warning-for-configured, quiet-suppression, and the C2 TOCTOU test (#45). It does **not** appear to cover: an *empty-string* `trusted_roots` entry (AC-11), a *relative* entry's cwd-dependence as an adversarial case (AC-10 is only tested as "resolves against cwd," not as a trust-widening hazard), or a Windows `PureWindowsPath("C:\\Users")` broad-detection assertion wired through the `configured` path. Treat these absences as corroborating signal for AC-10/AC-11/AC-19, not as separate findings.

---

## Agent Authorizations

| Agent | Authorized? | Technique allowlist (framing only — code review) | Rationale |
|-------|-------------|---------------------------------------------------|-----------|
| red-lead | Active (this doc) | Scope + RoE + attack-case authoring | Mandatory first agent |
| red-vuln | **Authorized** | CWE-20/22/59/73/367/426/1284 static + in-process/sandbox execution of AC-1..AC-21 against T-1..T-5 | Primary assessor |
| red-exploit | **Authorized (code-review mode only)** | PoC *test cases* against real functions in a disposable sandbox; NO live target, NO writes outside sandbox | Validate AC-2/AC-11/AC-12 repros if a second pass is wanted |
| red-reporter | **Authorized** | Aggregate, apply rubric, produce engagement report | Terminal reporting |
| red-recon, red-privesc, red-lateral, red-persist, red-exfil, red-social, red-infra | **NOT authorized** | — | Out of engagement type (white-box code review, no live systems/network/persistence/exfil/SE) |

**RoE-sensitive flags:** `social_engineering_authorized: false`, `persistence_authorized: false`, `exfiltration_authorized: false`. All gated OFF.

---

## Constitutional Compliance

- **P-001 (evidence-based):** Every attack case cites the exact function and line range in the shipped `da34a8b8` code (read directly from `containment_policy.py`, `project_root.py`, `ast_commands.py`, `env_config_adapter.py`), not the plan.
- **P-002 (persisted):** This attack plan is persisted at the BUG-010 engagement path; it is the load-bearing artifact red-vuln validates against.
- **P-003 (no recursive subagents):** red-lead authored this directly; delegates nothing recursively.
- **P-020 (user authority):** The owner's accepted Option C policy (declared-trust proceeds; `--root` discretion; broad-root allowed-with-warning) is respected as policy, not overturned. The plan recommends input-hygiene hardening; it does not mandate reversing owner decisions.
- **P-022 (no deception):** Cases are labeled as hypotheses to test, not confirmed findings. Expected-SAFE (positive-assurance) cases are called out as such. The one case red-lead pre-assesses as *likely* a real finding (AC-11) is stated plainly with its severity uncertainty (deployment/config-channel dependence) disclosed.

---

*red-lead re-check attack plan v2.0 — RED-BUG010, Option C @ da34a8b8. Methodology and plan only; no exploit executed, no code modified. Downstream: hand off to red-vuln (execute AC-1..AC-21), then red-reporter (severity + report).*
