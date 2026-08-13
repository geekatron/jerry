# Red Team Report: BUG-010 Option C — `jerry ast` Containment Redesign

**Strategy:** S-001 Red Team Analysis
**Deliverable:** `src/interface/cli/containment_policy.py`, `src/interface/cli/project_root.py`,
`src/interface/cli/ast_commands.py`, `src/interface/cli/parser.py`, `src/interface/cli/main.py`,
`src/interface/cli/adapter.py` (BUG-010 Option C), branch `fix/BUG-010-ast-project-root` @ `cce557c5`
**Criticality:** C4 (tournament, Group 3 of 6 -- Challenge)
**Date:** 2026-08-10
**Reviewer:** adv-executor (blind S-001 pass)
**H-16 Compliance:** N/A for this pass -- this is a blind, single-strategy execution inside a
6-group parallel tournament fan-out (self-refine -> steelman -> **challenge** -> verify -> decompose
-> score); the orchestrator enforces cross-group ordering, not this agent. No S-003 Steelman
artifact was supplied to this agent; findings below are reported honestly per P-022 without a
fabricated H-16 reference.
**Threat Actor:** A local, filesystem-capable adversary (co-resident process, malicious FUSE
mount, or a compromised dependency invoked mid-pipeline) who wants `jerry ast modify` (or
`ast_frontmatter`/`ast_parse`, transitively) to read or write a file **outside** the declared
containment roots (project root + `ast.trusted_roots`), while the CLI still reports success and
the operator/agent believes containment held. Capability: local write access to a directory the
target Jerry invocation will touch, or control over environment variables / config files in a
shared/CI deployment. Motivation: defeat the exact security property Option C was built to
restore (arbitrary file read/write via `jerry ast`, escaping the sandboxed project tree).

---

## Summary

Option C's headline claims (no auto-widened temp trust, structural not index-based classification,
a write-time TOCTOU recheck for `ast_modify`) hold under the single-swap and config-channel attacks
`red-vuln-option-c-findings.md` already tested and confirmed DISSOLVED. This pass targeted what that
report did **not** exercise: the exact mechanics of the write path inside `ast_modify()`, the
`is_broad` warning suppression logic, and the actual variable bound to the on-disk write target.
**One CRITICAL finding (RT-001)** shows the "C2 fix" — the write-time recheck — validates a
freshly-*re-resolved* path but the atomic write itself uses a *different, earlier-resolved* path
variable (`target_path`, captured before the recheck runs); a two-step symlink swap (out, then back)
defeats the recheck while the write still lands outside all allowed roots. This directly falsifies
the design doc's explicit claim that "a symlink swapped between the read and the write is caught."
Three further findings (two Major, two Minor) round out residual boundary/degradation gaps in the
`is_broad` warning path and the two-read config dependency. **Recommendation: REVISE** — RT-001 and
RT-003 (its parent-directory sibling) MUST be closed before merge; RT-002 SHOULD be closed in the
same change given how cheap the fix is (the `is_broad` value already exists per root).

---

## Findings Table

| ID | Attack Vector | Category | Exploitability | Severity | Priority | Defense | Affected Dimension |
|----|---------------|----------|-----------------|----------|----------|---------|--------------------|
| RT-001-20260810 | `ast_modify` write-time recheck validates a fresh resolve, but the actual write uses a stale, earlier-captured `target_path` -- two-step symlink swap bypasses the C2 fix | Boundary | Medium | Critical | P0 | Partial (ineffective) | Methodological Rigor / Internal Consistency |
| RT-002-20260810 | Broad-root warning (`is_broad`) is computed for the `project` classification but unconditionally suppressed, so a misconfigured/empty `CLAUDE_PROJECT_DIR` or a `/`-rooted cwd silently grants full-filesystem trust with zero signal | Degradation | Medium | Major | P1 | Missing | Completeness |
| RT-003-20260810 | Write-time containment re-validates only the leaf `file_path`; nothing re-verifies `target_path.parent` is still the same physical directory at `mkstemp`/`os.replace` time -- a parent-directory symlink swap escapes without ever touching the leaf-level check | Boundary | Low-Medium | Major | P1 | Missing | Completeness |
| RT-004-20260810 | Each `ast_modify` call performs two independent, full config-layer reads (`get_containment_roots()` at read time and again at write time), widening the RT-001 race window and creating an unrelated risk of mid-invocation config drift (concurrent `jerry config set`) | Dependency | Low | Minor | P2 | Missing | Evidence Quality |
| RT-005-20260810 | The R-3/R-4 transparency mechanism (Option C's stated visibility improvement) is suppressed by `--quiet`, which is precisely the flag the design's own primary caller (LLM/agent scratchpad pipelines piping JSON) is expected to pass, so the audience most likely to be operating under a widened trust store is least likely to see the warning | Ambiguity | Low | Minor | P2 | Missing | Traceability |

**Finding ID Format:** `RT-{NNN}-{execution_id}` where `execution_id` = `20260810` (session date).

---

## Finding Details

### RT-001: `ast_modify` write-time recheck validates a different path than it writes to [CRITICAL]

**Attack Vector:** In `ast_commands.py::ast_modify`, the sequence of operations is:

```
604   source, exit_code = _read_file(file_path, root, quiet)      # RESOLVE #1 (validated internally)
...
620   target_path = Path(file_path).resolve()                     # RESOLVE #2 -- captured, UNvalidated at this instant
...
634   if _ENFORCE_PATH_CONTAINMENT:
635       _, write_time_error = _check_path_containment(file_path, root, quiet=True)   # RESOLVE #3 (validated)
636       if write_time_error is not None:
637           print(...); return 2
...
644   temp_fd, temp_path_str = tempfile.mkstemp(dir=str(target_path.parent), ...)      # uses RESOLVE #2
654   os.replace(temp_path_str, str(target_path))                                       # uses RESOLVE #2
```

`_check_path_containment` (line 635) internally calls `Path(file_path).resolve()` **again**, a third,
independent resolution of the same mutable string `file_path`. Its return value's resolved-path
component is discarded (`_, write_time_error = ...`); only the pass/fail signal survives. The actual
write target, `target_path`, was captured earlier at line 620 -- *before* the recheck ever runs --
and is never reconciled with what the recheck validated. A single mutable input (`file_path`, a
symlink) is resolved three separate times across the function, at three separate moments, with no
guarantee any two resolutions agree.

**Category:** Boundary (gap between validation-time and use-time path resolution -- CWE-367,
TOCTOU race condition).

**Exploitability:** Medium -- requires an attacker with the ability to swap a symlink **twice**
within the narrow window between line 620 and line 635 (out to a target outside all allowed roots,
then back to something inside them), e.g. via a malicious FUSE filesystem, an inotify-triggered
symlink flipper, or a co-resident process racing the CLI invocation. The window is non-trivial:
between lines 604 and 635 the function parses the full markdown AST (`JerryDocument.parse`),
extracts frontmatter, and re-renders the document (`new_doc.render()`) -- real CPU work that widens
the race window measurably for larger documents, and RT-004 below shows the recheck itself performs
a second full config-file read, widening it further.

**Severity:** Critical -- this is a complete, silent bypass of the exact protection the C2 fix
("write-time recheck") exists to provide. Concretely:

1. `file_path` is a symlink initially pointing inside an allowed root. Read-time check (RESOLVE #1)
   passes; `source` is read.
2. Between line 604 and line 620, the attacker repoints the symlink to a target *outside* all
   allowed roots (e.g. a cron file, an SSH `authorized_keys`, another user's config).
3. Line 620 captures `target_path` = the outside location.
4. Before line 635 runs, the attacker repoints the symlink back to *any* location inside an allowed
   root (does not need to be the original target).
5. Line 635's recheck (RESOLVE #3) sees the symlink in its "safe" state and passes.
6. `mkstemp(dir=str(target_path.parent))` (line 644) and `os.replace(..., str(target_path))`
   (line 654) both operate on `target_path` from step 3 -- the outside location -- writing the
   modified document content there. `jerry ast modify` prints `"status": "modified"` and exits 0.

**Existing Defense:** Partial (ineffective as constructed). A write-time recheck exists and is
*intended* to close exactly this class of attack (per the design doc's C2 disposition: "Write-time
recheck now calls the *same* `_check_path_containment` routine used at read time... closing the
TOCTOU gap"). The mechanism is present but structurally decoupled from the value actually used for
the filesystem write.

**Evidence:** `ast_commands.py:604,620,634-638,644,654`; design claim at
`eng-lead-option-c-plan.md` Section 1.3 ("This makes read-time and write-time containment
**literally the same function call**... a symlink swapped between the read and the write is caught
because `_check_path_containment` re-resolves via `os.path.realpath()` fresh, every call") and
Section 3, row C2 ("**Fixed**... closing the TOCTOU gap"). **Corroborating test-coverage gap:**
`red-vuln-option-c-findings.md` AC-2 confirmed the *single*-swap case is caught (symlink swapped
once, from in-root to out-of-root, then the write-time recheck and full `ast_modify()` both observe
the *same* post-swap state and correctly reject) -- this is consistent with and does not contradict
RT-001, because a single swap never separates what RESOLVE #2 and RESOLVE #3 see. The plan's own
TDD list item #45 (`test_ast_modify_when_symlink_swapped_between_read_and_write_then_rejected_at_write_time`)
is also single-swap-shaped ("is repointed outside all allowed roots before the write executes") and
would pass against the current code without exercising the swap-then-swap-back sequence that
defeats it. Both the shipped code and its planned regression test give false confidence about this
exact scenario.

**Dimension:** Methodological Rigor (the plan's own stated verification claim is false for the
scenario it claims to close) and Internal Consistency (code behavior contradicts documented design
intent).

**Countermeasure:** Make `_check_path_containment` return the resolved path it validated, and have
`ast_modify` use *that exact value* (not a separately-captured `target_path`) for `mkstemp(dir=...)`
and `os.replace(...)`. Concretely: change the write-time call site to
`resolved_write_target, write_time_error = _check_path_containment(file_path, root, quiet=True)`
and use `resolved_write_target` (not `target_path`) for both the `mkstemp` `dir=` argument and the
final `os.replace` destination. This closes the validate/use mismatch. A fully hermetic fix would
additionally resolve the path once and hold an open file descriptor across the check-and-write
(`os.open(..., O_NOFOLLOW)` + `os.fstat`/write-by-fd) to eliminate the residual, much narrower race
between the final check and the syscall itself -- flag as a follow-on hardening item if descriptor-
based writes are out of scope for this pass.

**Acceptance Criteria:** A test exercising the swap-then-swap-back sequence (symlink: in-root ->
out-of-root -> back to in-root, all before the write-time recheck executes) MUST be added and MUST
show the write is rejected (or, if a benign target is restored, that the write lands on the value
the recheck actually validated, never on a value captured before the recheck ran). The fixed
`ast_modify` MUST use the return value of the write-time `_check_path_containment` call as the write
target, not a separately-resolved `target_path`.

---

### RT-002: Broad-root warning is computed but unconditionally suppressed for the `project` classification [MAJOR]

**Attack Vector:** `resolve_allowed_roots()` (`containment_policy.py:152-159`) computes
`is_broad=_is_broad_containment_root(project_root)` for the project-root `ContainmentRoot` entry
unconditionally -- the value is always populated. But `get_containment_roots()`'s warning loop
(`project_root.py:223-245`) only emits a warning for `classification == "explicit"` or
`"configured"`; the `"project"` branch is explicitly a no-op with the comment `# "project"
classification: no warning -- unchanged from prior behavior; the project root is always the user's
own repository by construction of get_project_root()`.

That "by construction" guarantee does not hold: `get_project_root()` (`project_root.py:40-54`)
returns `CLAUDE_PROJECT_DIR` (treating an empty string as unset) or falls back to `Path.cwd()` --
neither input is validated for broadness. A container with no `WORKDIR` set (cwd defaults to `/`),
a templated CI job that interpolates an unset variable into `CLAUDE_PROJECT_DIR=""`, or simply
invoking `jerry ast` from a shell that has `cd`'d to `$HOME` or `/`, all produce a project root that
IS broad by the code's own `_is_broad_containment_root` definition -- yet the one place that
detection result is computed, it is discarded specifically for this classification.

**Category:** Degradation (protection erodes silently as environment/config drifts) with a Boundary
component (the containment boundary itself becomes the filesystem root with no signal).

**Exploitability:** Medium -- does not require code-level attacker action, only an environment
precondition that is plausible in exactly the deployment model `jerry ast` targets (containerized/
CI/agent-orchestrated invocations where `CLAUDE_PROJECT_DIR` is environment-supplied, not
interactively chosen). An attacker who can influence environment variables or the invocation cwd in
a shared/CI context (the same deployment model red-vuln's AC-18 already treats as realistic for
`JERRY_PROJECT` traversal) can trigger this deliberately.

**Severity:** Major -- when triggered, the effective containment boundary becomes the entire
filesystem (or `$HOME`), silently, with **zero** stderr signal, even though the exact detection
mechanism (`is_broad`) that would catch this for `configured`/`explicit` roots already ran and
already flagged it as broad. This is not Critical because it requires an environmental
misconfiguration precondition rather than being reachable via a single crafted CLI argument; it is
not Minor because, once triggered, it silently defeats the entire Option C security narrative
("no directory is trusted unless the project owns it or the user explicitly configured it") for
every subsequent invocation in that environment.

**Existing Defense:** Missing. The detection value exists (`is_broad` is computed); the warning
path for it is deliberately absent for this one classification.

**Evidence:** `containment_policy.py:152-159` (`is_broad` computed for project root);
`project_root.py:223-245`, specifically the trailing comment at `:243-245` documenting the
deliberate omission; `project_root.py:40-54` (`get_project_root`, no validation of `cwd()` or
`CLAUDE_PROJECT_DIR` broadness).

**Dimension:** Completeness (Option C's stated protection -- "no directory is trusted unless..." --
has an unguarded gap in the one input path with the least validation).

**Countermeasure:** Extend the existing `configured`/`explicit` warning branch to also fire for
`classification == "project"` when `root.is_broad` is True, using wording that names the actual
source (`CLAUDE_PROJECT_DIR` vs. cwd fallback) so the operator can immediately see which input
produced the broad root, e.g.: `"Warning: the resolved project root '{path}' is an unusually broad
containment root (filesystem/drive root or home directory); jerry ast containment is effectively
disabled for this invocation. Check CLAUDE_PROJECT_DIR / current working directory."`

**Acceptance Criteria:** A test setting `CLAUDE_PROJECT_DIR` (or cwd, via monkeypatch) to a broad
path (e.g. `/` or a `PurePath` with `len(parts) <= 1`) and asserting the R-3-style warning fires on
stderr for the `project` classification, matching the coverage already required for `explicit` and
`configured` (per the plan's own test #26/#27 pattern).

---

## Recommendations

**P0 (MUST mitigate before acceptance):**
- **RT-001** -- Return and reuse the resolved path from the write-time `_check_path_containment`
  call as the actual `mkstemp`/`os.replace` target in `ast_modify`, eliminating the stale
  `target_path` variable. Add a swap-then-swap-back regression test. Acceptance criteria as stated
  in the finding detail above.

**P1 (SHOULD mitigate before acceptance, low cost relative to blast radius):**
- **RT-002** -- Extend the `is_broad` stderr warning to the `project` classification. Acceptance
  criteria as stated in the finding detail above.
- **RT-003** -- Re-verify (or fd-anchor) the target file's parent-directory identity at write time,
  not just the leaf file's symlink status. Minimal fix: after the write-time
  `_check_path_containment` call, additionally confirm
  `os.path.realpath(str(resolved_write_target.parent)) == str(resolved_write_target.parent)` (i.e.
  the parent itself is not a symlink introduced after `target_path` capture), or fold this into the
  RT-001 fd-anchored countermeasure, which closes both simultaneously.

**P2 (MAY mitigate, monitor):**
- **RT-004** -- Consider caching or single-sourcing the containment-roots resolution within one
  `ast_modify` invocation to reduce the number of independent config reads from two to one,
  narrowing the RT-001 race window as a secondary benefit. Not required if RT-001's fd-anchored fix
  is adopted (a single resolve-and-hold makes the second config read moot for the write path).
- **RT-005** -- Document explicitly (README/`--help` text) that `--quiet` suppresses the exact
  transparency mechanism Section L2 of the plan cites as the security-visibility benefit of Option
  C, and recommend that automated/agent callers log R-3/R-4 output to a side channel (e.g. a debug
  log) rather than suppressing it outright, so the visibility claim actually reaches its primary
  audience.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | RT-002, RT-003: the "no directory trusted unless project-owned or user-configured" claim has two unguarded gaps -- an unvalidated project-root input path and an unverified parent-directory identity at write time. |
| Internal Consistency | 0.20 | Negative | RT-001: shipped code directly contradicts the design doc's explicit, specific claim that write-time re-resolution "catches" a symlink swapped between read and write. |
| Methodological Rigor | 0.20 | Negative | RT-001: both the shipped code and its own planned regression test (#45) are shaped around a single-swap scenario; the deeper double-swap race that defeats the fix was neither implemented against nor tested for. |
| Evidence Quality | 0.15 | Negative | RT-004 shows the write-time recheck's "identical function call" framing undersells that it is a *second, independent* resolution+config-read, not a reuse of the first -- the deliverable's evidentiary claim about *what* is being re-verified is imprecise. |
| Actionability | 0.15 | Positive | All five countermeasures are concrete, line-anchored, and independently implementable; RT-001's fix (return-and-reuse the resolved path) is a small, mechanical change with a clear regression test. |
| Traceability | 0.10 | Neutral | Every finding cites exact file:line evidence in the shipped `cce557c5` source and cross-references the prior `red-vuln` report where relevant (RT-001 explicitly reconciles with AC-2 rather than contradicting it). |

**Overall assessment:** Targeted remediation required. RT-001 and RT-003 share a root cause (path
validated is not the path used) and can be closed together with one fd-anchored or return-value-
reuse fix in `ast_modify`; RT-002 is a one-branch addition to an existing warning loop. None of the
four findings reopen the six prior tournament Criticals (C1-C6) that `red-vuln-option-c-findings.md`
confirmed dissolved -- this report corroborates that conclusion for everything it re-examined
(single-swap TOCTOU, ownership-gate removal, temp-channel removal) and adds residual findings in the
narrower space those checks did not cover: the write-target binding inside `ast_modify`, and the
`is_broad` suppression asymmetry across classifications.
