# Red Team Report: BUG-010 `jerry ast` Containment Widening (PR #341, post-H-01/H-02 remediation)

**Strategy:** S-001 Red Team Analysis
**Deliverable:** `src/interface/cli/project_root.py`, `src/interface/cli/ast_commands.py`, `src/interface/cli/parser.py`, `src/interface/cli/main.py` on branch `fix/BUG-010-ast-project-root` (PR #341), plus `tests/unit/interface/cli/test_project_root.py` and `tests/unit/interface/cli/test_ast_commands.py`
**Criticality:** C4 (tournament, Group C)
**Date:** 2026-08-07
**Reviewer:** adv-executor (blind, Group C -- no visibility into other reviewers' outputs)
**H-16 Compliance:** S-003 Steelman artifact present in this directory (`adv-s003-steelman.md`) -- confirmed by file existence only; per the blind-agent isolation mandate for this tournament, its content was not read.
**Threat Actor:** An attacker with unprivileged write access to a directory Jerry treats as an allowed containment root by default -- `tempfile.gettempdir()` or `/tmp` -- on a host or execution environment where that directory (or its effective identity namespace) is shared with the victim: a shared/CI multi-tenant Linux host, a self-hosted CI runner processing multiple untrusted jobs, or a container/pod environment where multiple tenants share a UID. Goal: defeat the H-01 ownership gate (the remediation this specific pass exists to stress-test) to (a) read or inject content the gate is supposed to block, and/or (b) cause the victim's `jerry ast modify` invocation to overwrite a file it does not own. Capability: full source access (public repo), ability to create/replace files and symlinks in the shared containment root, and either repeatable/automatable invocation timing (CI pipelines, agent loops) or co-location in the same UID namespace (containers). Motivation: on a shared host this is direct cross-tenant read/write; in Jerry's specific AI-agent operating model, the same primitive doubles as a delivery mechanism for adversarial content into an LLM agent's context via `jerry ast` JSON output.

---

## Summary

The prior `/red-team` pass (red-lead + red-vuln) correctly identified and the deliverable correctly remediated H-01 (temp-root ownership gate) and H-02 (broad-root warning coverage). This pass targeted the two things the prompt specifically asked to probe: whether the H-01 gate can be defeated by racing it, and whether its own design assumptions hold. Both hold up worse than the prior REFUTED verdict on the adjacent H-05 (write-time TOCTOU) finding assumed. **7 attack vectors identified, 4 Critical, 2 Major, 1 Minor.** The headline result: the H-01 ownership gate is (1) checked via a separate `stat()` call that is not atomic with the subsequent read/write, and fails **open** on any `OSError` during that check -- an attacker-forceable, not merely lucky, bypass; (2) **never invoked at all** on the `ast_modify` write path, which independently re-resolves the target path a second time, meaning red-vuln's H-05 "os.replace does not follow a final-component symlink" REFUTED verdict rests on an inaccurate premise for this code (the symlink is dereferenced in Python via `Path.resolve()` *before* `os.replace` is ever called, so it is followed in effect); and (3) fundamentally assumes "different tenant implies different UID," an assumption that is false in Jerry's most plausible real multi-tenant deployment model -- containerized/self-hosted CI -- where cross-tenant jobs commonly share UID 0 or a fixed non-root UID. **Recommendation: REVISE.** The H-01 fix should not be considered closed; two of the four Critical findings (RT-002, RT-003) describe deterministic-not-probabilistic bypasses of the exact mechanism this remediation pass was meant to validate.

---

## Findings Table

| ID | Attack Vector | Category | Exploitability | Severity | Priority | Defense | Affected Dimension |
|----|---------------|----------|-----------------|----------|----------|---------|---------------------|
| RT-001-20260807T1500 | Ownership `stat()` and the actual content read/write are two separate, non-atomic, path-based syscalls -- classic TOCTOU window between validation and use | Boundary Violation | Medium | Critical | P1 | Partial | Methodological Rigor |
| RT-002-20260807T1500 | `_check_temp_root_ownership` fails **open** on any `OSError` during its `stat()` call -- an attacker can deliberately trigger the error (unlink the file at the right instant) to force a skip rather than merely win a race | Rule Circumvention | High | Critical | P0 | Missing | Internal Consistency |
| RT-003-20260807T1500 | `ast_modify`'s write path independently re-resolves the target a second time and never calls the ownership gate; this also invalidates the prior pass's H-05 REFUTED verdict on `os.replace` symlink safety | Boundary Violation | Medium | Critical | P0 | Missing | Evidence Quality |
| RT-004-20260807T1500 | Ownership gate assumes UID uniquely identifies a tenant; false under container/self-hosted-CI UID convergence (shared UID 0 or fixed non-root UID across untrusted jobs) | Dependency Attack | High (given deployment) | Critical | P0 | Missing | Completeness |
| RT-005-20260807T1500 | Windows path unconditionally skips the ownership check, relying on an unverified assumption that `%TEMP%` is always per-user; a shared/overridden `TEMP` env var on Windows CI silently defeats it | Dependency Attack | Low-Medium | Major | P1 | Missing | Completeness |
| RT-006-20260807T1500 | "Current user" is defined as `os.geteuid()` (effective UID) with no consideration of real/saved UID divergence or rootless-container UID-namespace remapping | Ambiguity Exploitation | Low | Minor | P2 | Missing | Methodological Rigor |
| RT-007-20260807T1500 | Practical protection strength decays under high-frequency automated invocation (CI/agent loops = many independent race trials); `--root` is independently re-resolved at read time and write time, producing two different allowed-root sets within one invocation if the `--root` argument traverses a symlink that changes mid-command | Degradation Path | Low | Minor | P2 | Partial | Traceability |

**Finding ID Format:** `RT-{NNN}-{execution_id}`, execution_id `20260807T1500` (this session).

---

## Finding Details

### RT-001: Ownership check is not atomic with the read/write it protects [CRITICAL]

**Attack Vector:** In `_check_path_containment` (`ast_commands.py:290-367`), the path is resolved once (`resolved = Path(file_path).resolve()`, line 326) and the H-01 ownership gate stats that same resolved path (`_check_temp_root_ownership`, called at lines 342-345, which itself calls `resolved.stat()` at `ast_commands.py:283`). The actual content read happens later, in `_read_file` (`ast_commands.py:402`, `resolved.read_text(...)`), as a **separate** syscall against the same path string. Nothing pins these two operations to the same inode (no `os.open()` + `os.fstat()` + `fdopen()`/`os.read()` pattern; both are path-based). An attacker with write access to the matched temp-default root (which, by definition of the widened default set, is world-writable) can unlink and recreate the file at the exact resolved path between the ownership `stat()` and the content read, so the content Jerry actually reads differs from the file whose ownership was verified.
**Category:** Boundary Violation
**Exploitability:** Medium -- the window between the two syscalls is only a few Python bytecode instructions wide for non-modify commands (`ast_parse`, `ast_frontmatter`, `ast_query`, etc.), but classic TOCTOU races of this width are a well-established, reliably-automatable exploitation technique (tight-loop unlink/recreate), and the window widens substantially for `ast_modify` because markdown parsing and mdformat rendering occur between the read and the (separately vulnerable, see RT-003) write-time resolve.
**Severity:** Critical -- Jerry's own output model turns this into more than a data-integrity nuisance. `jerry ast parse`/`frontmatter`/`query` JSON output is the primary channel an AI coding agent (Claude Code) consumes. An attacker who plants a world-readable, adversarially-crafted markdown file in the shared temp root and wins the race gets that content ingested under the appearance of an ownership-verified file, which is a TOCTOU-enabled prompt-injection delivery vector into the calling agent's context -- not merely a file-confusion bug.
**Existing Defense:** Partial -- the ownership gate exists and is correctly scoped to temp-default matches, but it validates identity at a point in time disconnected from the point of use.
**Evidence:** `ast_commands.py:283` (`resolved.stat().st_uid != os.geteuid()`), `ast_commands.py:326` (first resolve), `ast_commands.py:402` (`resolved.read_text(...)`, the same `resolved` object reused but via a fresh syscall). No file descriptor is opened once and reused for both the ownership check and the read.
**Dimension:** Methodological Rigor -- the H-01 fix was validated (by the prior red-team pass) as "present," not as "atomic with its target," which is the property that actually determines whether it can be relied on as a security boundary rather than a best-effort speed bump.
**Countermeasure:** Open the resolved path once via `os.open()` (POSIX `O_NOFOLLOW` where the resolved path is expected to already be a non-symlink terminal target), `os.fstat()` the open file descriptor for the ownership check, and read via that same descriptor (`os.fdopen(fd).read()`). This closes the TOCTOU window structurally rather than narrowing it probabilistically.
**Acceptance Criteria:** A test demonstrating that the file whose ownership is validated is provably the same inode as the file whose content is returned, e.g. by asserting the check and the read share a single `os.stat_result.st_ino` obtained from one open file descriptor, not two independent path-based stats.

---

### RT-002: Fail-open on `OSError` turns the ownership gate into an attacker-forceable no-op [CRITICAL]

**Attack Vector:** `_check_temp_root_ownership` (`ast_commands.py:244-287`) contains:
```python
try:
    if resolved.stat().st_uid != os.geteuid():
        return f"Path in shared temp directory is owned by another user: {file_path}"
except OSError:
    pass  # Fail open on stat error; the size-check stat() below still applies.
```
This is documented as intentional and consistent with the size-check's own OSError handling. But the size-check's fail-open is benign (a missing file just proceeds to the existing "file not found" handling downstream); the ownership gate's fail-open is not benign -- it is the **entire security control** for this code path, and any `OSError` during its own verification step causes the control to silently pass rather than reject. An attacker with write access to the shared temp root does not need to win a probabilistic race against the read: they can *deliberately* cause the `stat()` call to raise (unlink the target file at the moment Jerry calls `_check_temp_root_ownership`, or engineer a transient `ENOENT`/`EACCES`/`ELOOP` condition), which unconditionally clears the gate, and then place their own content at that path before the subsequent read (RT-001) executes.
**Category:** Rule Circumvention
**Exploitability:** High -- unlike RT-001's tight timing window, this does not require a lucky race outcome; forcing an `OSError` is a deterministic action available to anyone who can `unlink()` or otherwise perturb the target path, converting the exploit from probabilistic to attacker-controlled.
**Severity:** Critical -- it defeats H-01 in the direction that matters most (denies the check ever firing) rather than merely racing it.
**Existing Defense:** Missing -- there is no compensating control for a stat failure specifically on the ownership-check path; the code explicitly chooses to proceed.
**Evidence:** `ast_commands.py:280-287`, especially the bare `except OSError: pass` at line 285-286, and the surrounding docstring's own admission ("fails open on `OSError`... consistent with the size check... which applies its own handling") -- a design rationale that does not distinguish "fail open is fine here" (size limit) from "fail open defeats the control" (ownership gate).
**Dimension:** Internal Consistency -- the module applies one fail-open policy uniformly across two checks with materially different consequences of failing open.
**Countermeasure:** Fail **closed** specifically for the ownership gate: any `OSError` raised while attempting to verify ownership of a temp-default-root match should be treated as "cannot verify ownership -- reject," not "ownership unverifiable -- proceed." The size check may retain its existing fail-open behavior (it is not a security boundary), but the two should no longer share a rationale.
**Acceptance Criteria:** A test that monkeypatches `Path.stat` to raise `OSError` for a temp-root-matched file and asserts the containment check now **rejects** (currently the corresponding test, `test_check_temp_root_ownership_when_stat_oserror_then_fails_open`, asserts the opposite -- that test will need to be inverted, and its name updated, as part of the fix).

---

### RT-003: `ast_modify`'s write path never re-runs the ownership gate, and independently re-resolves the target -- the prior pass's H-05 REFUTED verdict does not hold for this code [CRITICAL]

**Attack Vector:** `ast_modify` (`ast_commands.py:637-724`) calls `_read_file` once (line 659), which performs the H-01 ownership-gated containment check against a `resolved` path computed *inside* `_check_path_containment`. That `resolved` Path object is never returned to `ast_modify`. Instead, `ast_modify` independently recomputes the write target from the raw string argument:
```python
target_path = Path(file_path).resolve()  # line 675, a SECOND, independent resolve
if _ENFORCE_PATH_CONTAINMENT:
    allowed_roots = get_containment_roots(root)  # line 679, fresh containment set
    if not any(target_path.is_relative_to(r) for r in allowed_roots):
        return 2
# ... mkstemp + os.replace(temp_path_str, str(target_path))   # lines 688-698
```
This recheck validates **containment** (is `target_path` still under an allowed root) but never calls `_check_temp_root_ownership` -- the ownership gate simply does not exist on the write path. Worse, because `target_path` is computed via a fresh `Path.resolve()` call, if the file at `file_path` was swapped for a symlink between the read (line 659) and this second resolve (line 675) -- a realistic window, widened by the markdown parse/render work that happens in between (lines 663-672) -- `target_path` becomes whatever that symlink points to **at that later moment**, fully dereferenced in Python before `os.replace` is ever invoked. This directly contradicts the prior pass's H-05 REFUTED reasoning ("`os.replace` uses atomic rename semantics -- replaces the symlink itself, does not follow a final-component symlink to write through it"): that property is a fact about the raw `rename(2)` syscall when given a symlink *path*, but this code never passes `os.replace` a symlink path -- it passes the already-dereferenced `target_path`, so the symlink **is** followed, in Python, before the OS-level guarantee the prior finding relied on ever comes into play. An attacker who controls the containing directory (e.g. their own subdirectory created inside the shared temp root, which is not sticky-bit-protected the way `/tmp` itself is) can therefore get the victim's `jerry ast modify` invocation to overwrite an arbitrary other file within the same allowed containment root that the victim does not own -- an arbitrary-file-overwrite primitive, not merely a read-side information leak.
**Category:** Boundary Violation
**Exploitability:** Medium -- requires winning a race against a window that includes non-trivial CPU work (parse + mdformat render), which is a materially easier target than a bare syscall gap, and the attack is retryable indefinitely against any automated/CI-driven `jerry ast modify` invocation.
**Severity:** Critical -- integrity impact on files the victim does not own, reachable under default configuration (no `--root`, no env override) on the exact deployment model (shared/CI multi-tenant temp root) the H-01 fix exists to protect.
**Existing Defense:** Missing on the ownership axis (containment-only recheck exists, per WI-020/M-21, but that is orthogonal to H-01).
**Evidence:** `ast_commands.py:659` (read, internally ownership-gated), `ast_commands.py:675` (second, independent, ownership-blind resolve), `ast_commands.py:678-682` (containment-only recheck), `ast_commands.py:688-698` (mkstemp + os.replace against the ownership-blind `target_path`). Cross-reference: `red-vuln-findings.md` H-05 verdict text, which characterizes `os.replace` as "not following a final-component symlink" without accounting for the prior `Path.resolve()` call that already dereferenced it.
**Dimension:** Evidence Quality -- this finding is itself evidence that the prior pass's REFUTED verdict for H-05 was reached without tracing the actual symlink-dereferencing sequence in this specific code, only the general `os.replace` contract.
**Countermeasure:** (1) Have `_read_file` return the validated `resolved` Path alongside the content, and have `ast_modify` reuse that exact object as `target_path` rather than recomputing it -- this alone removes the double-resolve race. (2) Independently, re-run `_check_temp_root_ownership` (not just containment) in the write-time recheck, scoped identically to the read-time gate (temp-default matches only), so even a same-path race cannot silently drop the ownership requirement between read and write.
**Acceptance Criteria:** A test in which the file at `file_path` is replaced with a symlink to a second, differently-owned file (both under an allowed temp root) between the `_read_file` call and the write; the write must be rejected, not silently redirected to the second file. A second test confirming `ast_modify`'s write-time recheck calls the same ownership-gate function as the read-time check for temp-default matches.

---

### RT-004: The ownership gate's entire premise -- distinct UID implies distinct tenant -- fails under container/self-hosted-CI UID convergence [CRITICAL]

**Attack Vector:** `_check_temp_root_ownership` treats `os.geteuid()` as a reliable proxy for "which principal is running this process," and treats a UID match as proof the file belongs to the same trust domain. This holds for the deployment model red-vuln explicitly modeled (distinct human OS accounts on a shared Linux host) but not for what is arguably Jerry's more realistic multi-tenant surface: containerized CI. Two common, unremarkable configurations defeat the check with zero additional attacker capability: (a) multiple CI jobs from **different**, mutually untrusted repositories/PRs run in separate containers that all default to UID 0 (root) inside the container -- a very common default for CI action images -- and share a host-level `/tmp` or bind-mounted temp volume; (b) self-hosted GitHub Actions runners (this very repository's `jerry ci` namespace exists to support CI automation) processing multiple jobs under one shared service-account UID, a documented, well-known GitHub Actions self-hosted-runner risk. In either case `os.geteuid()` returns the **same value for every tenant**, so `_check_temp_root_ownership`'s comparison is always true regardless of who actually owns the file -- the gate is not merely bypassable, it never differentiates tenants at all in this deployment shape.
**Category:** Dependency Attack (the control depends on an environmental invariant -- "1 UID = 1 tenant" -- that the code never verifies and that its stated deployment context, CI, is prone to violating)
**Exploitability:** High, conditioned on deployment -- trivial and requires zero race-winning or timing precision once the shared-UID precondition holds; this is strictly easier to exploit than RT-001/RT-002/RT-003, it simply requires the (common) deployment shape.
**Severity:** Critical -- this is not a corner case of the fix, it is a scenario where the fix provides **zero** protection while giving every appearance of having closed the gap (the check "runs," returns "match," and proceeds) -- a false sense of security is worse than an acknowledged absence of a control.
**Existing Defense:** Missing -- no code path considers container/namespace UID mapping, and the remediation's own documentation only frames the shared-host scenario in terms of "another user," implicitly assuming distinct human accounts.
**Evidence:** `ast_commands.py:280-287` (`os.geteuid()` as the sole identity signal, unconditionally); `project_root.py:43` and surrounding module docstring, which frames the entire widening in terms of "Claude Code scratchpad writes" -- an explicitly agent/automation-driven, frequently containerized or CI-orchestrated use case, not a manually-operated shared workstation.
**Dimension:** Completeness -- the deployment-model analysis in the H-01 remediation covers "single-user laptop" vs. "shared/CI multi-tenant host" as if the latter is adequately addressed by a UID check, without covering the UID-convergence sub-case that is common specifically in the CI/container half of that same category.
**Countermeasure:** Document this as an explicit, acknowledged residual risk (not a silent gap) in the same place H-01's remediation is documented, and, if containerized-CI becomes a material deployment target, evaluate a stronger per-invocation binding (e.g., an ephemeral, Jerry-generated marker/lockfile under the resolved path at command start, checked for exclusive ownership by the invoking process rather than by OS UID) rather than relying on `st_uid` at all in that mode.
**Acceptance Criteria:** A documented, explicit statement (in code comment and/or ADR) that the ownership gate does not protect same-UID multi-tenant deployments (containers sharing UID 0, self-hosted runners under one service account), so downstream operators do not mistake "H-01 fixed" for "safe on any shared CI runner."

---

### RT-005: Windows ownership-check skip is an unverified assumption, not a verified invariant [MAJOR]

**Attack Vector:** `_check_temp_root_ownership` unconditionally returns `None` (no check) when `os.name == "nt"`, justified by the docstring's claim that Windows' per-user `%TEMP%` (`C:\Users\<user>\AppData\Local\Temp`) "already structurally isolates temp directories by user under normal, non-elevated sessions." The code never verifies this at runtime -- it trusts the environment unconditionally. `tempfile.gettempdir()` on Windows resolves through the `TMP`/`TEMP`/`USERPROFILE`-derived environment variables, which can be overridden. A Windows CI runner (this repo's CI matrix, per the prior pass's own note, already runs `windows-latest`) that sets a shared `TEMP` env var pointing at a non-per-user path (a documented pattern in some self-hosted Windows CI/build-farm configurations, and in Windows containers where the per-user profile isolation this remediation relies on is weaker or absent depending on the container base image and isolation mode) silently reintroduces the exact same exposure H-01 closes on POSIX, with **no fallback check at all** -- not even a degraded one.
**Category:** Dependency Attack
**Exploitability:** Low-Medium -- requires either a misconfigured/shared Windows CI environment or a Windows container deployment; not reachable from a stock GitHub-hosted `windows-latest` job (fresh VM per job), but plausible on self-hosted Windows infrastructure.
**Severity:** Major -- weakens the guarantee without providing evidence the assumption it substitutes actually holds in the operator's environment; not Critical because the default GitHub-hosted CI case is not affected.
**Existing Defense:** Missing -- by design (`os.name == "nt": return None`), with no runtime verification of the per-user-isolation assumption it relies on.
**Evidence:** `ast_commands.py:280-281`; docstring at `ast_commands.py:260-264` ("Windows' per-user `%TEMP%`... already structurally isolates temp directories by user under normal, non-elevated sessions, so this check is a deliberate no-op there rather than an oversight").
**Dimension:** Completeness -- the H-01 remediation is only verified for the POSIX branch; the Windows branch is asserted, not tested against the failure mode it dismisses.
**Countermeasure:** At minimum, document the assumption's precondition explicitly ("this assumes `%TEMP%` has not been overridden to a shared location") next to the `os.name == "nt"` branch. If a stronger guarantee is wanted, compare the resolved temp root's owner (via `win32security`, as red-vuln's own remediation note for H-01 already floats and rejects as disproportionate) only when the resolved root is *not* a subpath of `%USERPROFILE%`, limiting the new dependency to the uncommon case rather than the common one.
**Acceptance Criteria:** A code comment or ADR note stating the precondition under which the Windows no-op is safe, so a future operator overriding `TEMP` in a shared Windows CI context has a documented signal this control does not apply there.

---

### RT-006: "Current user" is defined only as effective UID, an ambiguous identity signal [MINOR]

**Attack Vector:** The ownership gate's notion of identity is exactly `os.geteuid()` -- the process's effective UID. This does not consider the real UID, saved-set UID, or (in rootless-container UID-namespace setups) the host-visible UID that may differ from the UID the process itself believes it has. In most direct-invocation scenarios these coincide, but any wrapper, sandbox, or privilege-transition tooling that changes effective UID without the process's own awareness could make the check compare against an identity that is not the one an operator would intuitively mean by "the current user."
**Category:** Ambiguity Exploitation
**Exploitability:** Low -- requires a non-default execution wrapper; not reachable via the documented, direct-CLI invocation path.
**Severity:** Minor -- theoretical under Jerry's documented usage model; worth naming so it is not later assumed away.
**Existing Defense:** Missing -- the term is used without a defined scope.
**Dimension:** Methodological Rigor.
**Countermeasure:** State explicitly (docstring) that "current user" means `os.geteuid()` specifically, and that any invocation path where effective UID does not represent the operator's true identity (setuid wrappers, some sandboxes) is out of scope for this gate.

---

### RT-007: Protection strength decays under repeated automated invocation; `--root` is resolved twice with no consistency guarantee [MINOR]

**Attack Vector:** Every attack that depends on winning a race (RT-001, RT-003) becomes a near-certainty, not a low-probability event, under Jerry's actual usage pattern: `jerry ast` commands are frequently invoked by automated agents and CI pipelines at high frequency, giving an attacker effectively unlimited independent trials rather than one shot. Separately, `get_containment_roots(root)` is called independently at read time (inside `_check_path_containment`, via `_read_file`) and again at write time (`ast_commands.py:679`) in `ast_modify`. If `--root` itself is, or traverses, a symlink whose target changes between these two calls, the two calls can resolve to different allowed-root sets within a single command invocation.
**Category:** Degradation Path
**Exploitability:** Low standalone (this is an amplifier for RT-001/RT-003, not an independent primitive), but raises their effective severity.
**Severity:** Minor as an isolated finding; documented separately from RT-001/RT-003 because it changes how those findings should be weighed (probabilistic-and-rare vs. probabilistic-and-eventually-certain).
**Existing Defense:** Partial -- the write-time recheck exists and would catch a widening/narrowing that moved `target_path` fully outside all roots, but does not guarantee the same root set was used for both checks.
**Dimension:** Traceability.
**Countermeasure:** Resolve `--root` once per invocation and thread the single resolved value through both the read-time and write-time checks, rather than calling `get_containment_roots()` twice.

---

## Recommendations

**P0 (MUST mitigate before acceptance):**
- **RT-002:** Change `_check_temp_root_ownership`'s `OSError` handling from fail-open to fail-closed for the ownership axis specifically (retain fail-open only for the unrelated size-limit check).
- **RT-003:** Thread the already-validated `resolved` Path from `_read_file`/`_check_path_containment` into `ast_modify`'s write path instead of recomputing it, and re-run the ownership gate (not just containment) at write time.
- **RT-004:** At minimum, document the same-UID multi-tenant limitation explicitly next to the H-01 remediation so it is a known, acknowledged residual risk rather than an implicit, unverified assumption.

**P1 (SHOULD mitigate):**
- **RT-001:** Move to a single-open, fd-based stat+read sequence to structurally close the ownership-check-to-content-read TOCTOU window.
- **RT-005:** Document the `%TEMP%`-per-user precondition the Windows no-op relies on.

**P2 (MAY mitigate / monitor):**
- **RT-006:** Document the effective-UID scope of "current user."
- **RT-007:** Resolve `--root` once per invocation; reuse across read-time and write-time checks.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | RT-003, RT-004: the H-01 remediation covers the read path and the single/distinct-UID case, but not the write path or the same-UID multi-tenant (container/CI) case -- both squarely within the "shared/CI multi-tenant host" scenario the remediation itself names as its target. |
| Internal Consistency | 0.20 | Negative | RT-002: the module applies one fail-open rationale to two checks (size limit, ownership) with materially different security consequences of failing open. RT-003 also surfaces an inconsistency between the prior pass's H-05 REFUTED verdict text and this code's actual symlink-dereferencing sequence. |
| Methodological Rigor | 0.20 | Negative | RT-001, RT-006: the ownership gate was validated as "present" rather than "atomic with its target" or "well-scoped in its identity definition." |
| Evidence Quality | 0.15 | Negative | RT-003 specifically: the prior pass's H-05 REFUTED verdict is evidence-thin for this exact code path (relies on `os.replace`'s general contract, not the actual `Path.resolve()`-before-`os.replace` sequence in `ast_modify`). |
| Actionability | 0.15 | Positive | All P0/P1 countermeasures are concrete, minimal, and scoped identically to how H-01/H-02 were originally remediated (temp-default-match-only, no change to project-root or `--root` user-discretion paths). |
| Traceability | 0.10 | Neutral | Every finding cites exact file/line evidence; RT-007 is itself a traceability-adjacent finding about read/write root-resolution consistency. |

---

## Execution Statistics
- **Total Findings:** 7 (RT-001 through RT-007)
- **Critical:** 4 (RT-001, RT-002, RT-003, RT-004)
- **Major:** 1 (RT-005)
- **Minor:** 2 (RT-006, RT-007)
- **Protocol Steps Completed:** 5 of 5 (Threat Actor defined; Attack Vectors enumerated across all 5 categories with 7 vectors; Defense Gaps assessed with P0/P1/P2 prioritization; Countermeasures developed for all P0/P1 findings; Synthesis and Scoring Impact completed per H-15 self-review).
