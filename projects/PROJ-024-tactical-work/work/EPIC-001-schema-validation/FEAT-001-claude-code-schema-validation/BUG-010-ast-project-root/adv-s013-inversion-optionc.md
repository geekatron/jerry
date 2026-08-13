# Inversion Report: BUG-010 Option C — `jerry ast` Containment Redesign

**Strategy:** S-013 Inversion Technique
**Deliverable:** `eng-lead-option-c-plan.md` + implementation (`containment_policy.py`, `project_root.py`, `ast_commands.py`, `parser.py`, `main.py`, `adapter.py`) @ branch `fix/BUG-010-ast-project-root` `cce557c5`
**Criticality:** C4
**Date:** 2026-08-10
**Reviewer:** adv-executor (blind, Group 5 of 6 — Decompose)
**H-16 Compliance:** S-003 Steelman assumed applied in an earlier tournament group per the documented 6-group order (self-refine → steelman → challenge → verify → decompose → score); this execution is blind to that output and did not consume it directly.
**Goals Analyzed:** 7 | **Assumptions Mapped:** 8 | **Vulnerable Assumptions:** 6

---

## Summary

Inverting the deliverable's goals ("how would we *guarantee* this containment fails, ships broken, or silently burns the user?") surfaces one dominant root cause with two Critical consequences, plus four secondary Major/Minor gaps. The dominant root cause: the redesign's threat model (multi-tenant/shared OS temp) is real and explicitly discussed for the *removed* auto-trust path (C3/C4), but the *new* `ast.trusted_roots` mechanism has no equivalent guard against a user re-declaring that exact same shared-temp class of directory — and the design's own stated primary use case (Claude Code scratchpad) structurally pressures users toward doing exactly that. A second Critical finding shows the C6 `--quiet` fix is opt-in/default-off and is not adopted anywhere in Jerry's own canonical `jerry ast` documentation or agent definitions (verified directly, including this very agent's own definition), so the "Fixed" disposition for C6 does not hold under the project's real, current invocation patterns. Recommendation: **REVISE** — mitigate IN-001 and IN-002 before merge; IN-003–IN-006 may proceed as tracked follow-ups with explicit disclosure (consistent with the plan's own transparency precedent for the session-local config gap).

---

## Findings Table

| ID | Assumption / Anti-Goal | Type | Confidence | Severity | Evidence | Affected Dimension |
|----|------------------------|------|------------|----------|----------|--------------------|
| IN-001-20260810T1500 | "Requiring explicit `ast.trusted_roots` configuration is sufficient to prevent users from re-widening trust to shared/multi-tenant OS temp" | Assumption | Low | **Critical** | `project_root.py:169-171` docstring recommends declaring the scratchpad dir via `ast.trusted_roots`; `_is_broad_containment_root` (`containment_policy.py:53-107`) only flags fs-root/home-ancestor, never shared-temp ancestry (e.g. `/tmp`, `/private/tmp/claude-502`); red-vuln AC-16 confirms broadness testing covered only `/`, `$HOME`, home-parent — never a shared-temp shape | Methodological Rigor |
| IN-002-20260810T1500 | "The C6 `--quiet` fix resolves the merged-stream JSON-corruption risk in practice" | Anti-Goal | N/A | **Critical** | `parser.py`/`main.py` wire `--quiet` (default `False`) on all 10 subcommands; `skills/ast/SKILL.md` (canonical usage doc) never mentions `--quiet` in any example; `skills/adversary/agents/adv-executor.md` (this agent's own definition) invokes `jerry ast frontmatter/parse/validate` with no `--quiet` | Completeness |
| IN-003-20260810T1500 | "TOCTOU is closed by the `ast_modify` write-time recheck" (C2 disposition = Fixed) | Assumption | Medium | Major | `_read_file` (`ast_commands.py:284-325`) has no equivalent re-check between `_check_path_containment` and `resolved.read_text()`; only `ast_modify`'s write path (line 635) got the re-verification; TDD list (Section 4) has test #45 for write-time swap, none for read-time; not listed as a residual in Section 3's C1-C6 table (unlike the session-local config gap, which the plan explicitly discloses) | Internal Consistency |
| IN-004-20260810T1500 | "`get_project_root()`'s cwd/`CLAUDE_PROJECT_DIR` resolution is a safe, unambiguous anchor for the *new* trust-config lookup" | Assumption | Medium | Major | `project_root.py:40-54` — no upward `.git`/`pyproject.toml` boundary search; `build_layered_config_adapter()` derives `root_config_path`/`project_config_path` directly from this same value (`project_root.py:85-112`); table in Section 1 marks `get_project_root()` "UNCHANGED", but its blast radius changed from "does a project exist here" to "which `.jerry/config.toml` (and therefore which `ast.trusted_roots`) governs this invocation" | Completeness |
| IN-005-20260810T1500 | "Windows behavior parity is established" for C1-C6 | Assumption | Medium | Minor | red-vuln AC-19/20/21 explicitly state "did NOT execute on a live win32 interpreter" (reasoning/same-flavor-mock only); `.github/workflows/ci.yml:247-263` DOES run a `windows-latest` matrix job (mitigating), but Section 7's DD-1–DD-4 owner sign-off table has no explicit "confirm windows-latest CI green" merge gate | Evidence Quality |
| IN-006-20260810T1500 | "Config-value input hygiene is complete" (relative paths warned, blanks dropped, traversal blocked) | Assumption | High | Minor | `_load_trusted_roots()` (`project_root.py:115-144`) only filters blank/whitespace via `str(entry).strip()`; a non-string TOML entry (int/bool) or an env-coerced numeric/boolean single value (`EnvConfigAdapter._parse_value`, `env_config_adapter.py:98-149`) silently degrades to an inert non-matching path rather than a fail-closed rejection, inconsistent with the fail-closed precedent already set for `JERRY_PROJECT` traversal (`project_root.py:94-105`) | Internal Consistency |

**Finding ID Format:** `IN-{NNN}-{execution_id}`, `execution_id = 20260810T1500`.

---

## Finding Details

### IN-001: Shared-temp re-widening via `ast.trusted_roots` is invisible to the broad-root warning, and the scratchpad use case pressures users into it [CRITICAL]

**Type:** Assumption
**Original Assumption:** The mandate's core claim — "No directory is trusted unless the project owns it or the user explicitly configured it" — is treated as sufficient protection because trust now requires a deliberate, visible user action (`ast.trusted_roots` entry) instead of silent auto-widening.

**Inversion:** What if the *only realistic way* to make the tool usable for its own stated primary use case forces the user into declaring the exact class of directory (shared, multi-tenant OS temp) that the redesign was built to stop auto-trusting — with zero warning distinguishing that choice from a genuinely private directory?

Concretely: Claude Code's scratchpad convention allocates a **new, randomly-named directory per session** (e.g. this very session's scratchpad path follows the pattern `/private/tmp/claude-<pid>/<workspace-hash>/<session-uuid>/scratchpad`). `project_root.py`'s own docstring (lines 169-171) tells the user: *"To grant `jerry ast` access to a scratchpad directory... declare it explicitly via `ast.trusted_roots`."* Given the per-session UUID, the user faces exactly two options, both bad:

1. **Reconfigure `ast.trusted_roots` every session** to the new UUID path — operationally infeasible for an agent-driven workflow, so in practice this option is abandoned quickly.
2. **Configure a shared ancestor** (`/private/tmp/claude-<pid>/`, or worse, `/tmp`/`/private/tmp` outright) to avoid per-session churn — which re-introduces the *exact* directory class (shared, multi-tenant, effectively world-writable-by-any-local-process OS temp) that C3/C4/C5 in the tournament attacked, and that this redesign's entire premise (Section 3, C5 disposition: *"Dissolved by design... `TMPDIR`/`TEMP` env vars have zero effect on `jerry ast` containment"*) claims is now eliminated.

`_is_broad_containment_root` (`containment_policy.py:53-107`) — the *only* signal a user gets about an unusually dangerous trust grant — checks exactly two shapes: filesystem/drive root (`len(parts) <= 1`) and home-directory-or-ancestor. It has **no concept of "well-known shared OS temp"**. Configuring `ast.trusted_roots = ["/tmp"]` or `["/private/tmp"]` produces **zero warning** — not even the DD-1 symmetry extension the design added specifically to give `configured` roots parity with `--root`'s R-3 warning. red-vuln's own AC-16 test matrix (broad-root coverage) confirms this gap by omission: it tests `/`, `$HOME`, and `$HOME`'s parent — never a shared-temp shape.

**Plausibility:** High. This is not a contrived attacker scenario; it is the design's own documented recommended workaround for its own stated primary use case, and it is directly reachable from information present in this very tournament's own environment (the scratchpad path pattern is literally visible in the session context every agent operates in).

**Consequence:** If a user or an autonomous agent (which may reasonably decide "just trust the whole `/private/tmp/claude-<pid>/` tree, it's simpler") makes this configuration choice, the entire threat model the tournament's C3/C4 findings addressed (foreign-UID/multi-tenant file planted in shared temp) is reopened — with **no remaining defense in depth**, because DD-2's recommended disposition is to **remove** `_check_temp_root_ownership` entirely (its rationale being "configured roots are never auto-trusted, they are deliberate declarations" — which is exactly the assumption this inversion breaks). This also means Section 3's "Dissolved by design" disposition for C3 and C4 is **conditional on a user behavior the design itself steers users away from following safely**, not an unconditional property of the code.

**Evidence:** `project_root.py:169-171` (docstring recommending `ast.trusted_roots` for scratchpad use); `containment_policy.py:53-107` (`_is_broad_containment_root` definition — no shared-temp branch); `eng-lead-option-c-plan.md` Section 3, C3/C4/C5 rows and DD-2 rationale; red-vuln-option-c-findings.md AC-16 (broadness test matrix, no shared-temp case tested).

**Dimension:** Methodological Rigor (the "broad root" heuristic's threat model is incomplete relative to the tournament's own established threat categories).

**Mitigation:** (a) Extend `_is_broad_containment_root` (or add a sibling check) to flag well-known OS temp roots (`tempfile.gettempdir()`'s resolved value and its immediate parent, `/tmp`, `/var/tmp` on POSIX, `%TEMP%`/`%TMP%` resolved value on Windows) as broad/warned for `configured` classification — symmetric to the DD-1 extension already made for home/fs-root. (b) Provide an ergonomic, safe alternative to per-session reconfiguration for the scratchpad use case specifically — e.g., a documented convention for a **stable** scratchpad parent directory Claude Code (or the invoking harness) creates once and reuses across sessions, so users are never operationally pressured toward configuring a shared/world-visible temp ancestor. (c) If DD-2 proceeds with full ownership-gate removal, retain *some* fail-closed defense specifically for `configured` roots whose resolved path matches a known-shared-temp pattern.

**Acceptance Criteria:** A new test asserting `ast.trusted_roots = ["/tmp"]` (or the platform-equivalent) produces a broad-root warning identical in spirit to the R-3/DD-1 mechanism; a documented, tested, low-friction scratchpad-trust pattern that does not require configuring a shared OS temp ancestor.

---

### IN-002: `--quiet` is opt-in/default-off and unused by Jerry's own canonical `jerry ast` usage patterns — C6's "Fixed" disposition does not hold in practice [CRITICAL]

**Type:** Anti-Goal (the anti-goal being tested: "how would we guarantee the C6 fix doesn't actually protect the primary caller?")

**Original Assumption:** Section 3's C6 disposition states **Fixed**: *"New `--quiet` flag (default `False`, i.e. warnings ON by default per the mandate)... suppresses both R-3... and R-4... stderr output for the invocation."*

**Inversion:** The fix exists and functions correctly in isolation (confirmed by red-vuln AC-6: quiet suppresses stderr without changing exit codes). But the fix is **opt-in** — every one of the 10 `jerry ast` subcommands defaults `quiet=False`, meaning the exact failure mode C6 describes (a stderr note corrupting a merged/naively-concatenated JSON stream) still fires **by default**, unless the caller explicitly passes `--quiet`. Two concrete, directly-verifiable pieces of evidence show Jerry's own canonical callers do not do this:

1. `skills/ast/SKILL.md` — the framework's own reference documentation for `jerry ast` usage — contains zero occurrences of `--quiet` across all of its command reference sections and worked examples (`jerry ast frontmatter`, `jerry ast modify`, `jerry ast validate`, `jerry ast render`, `jerry ast reinject`, `jerry ast parse`, `jerry ast query`).
2. `skills/adversary/agents/adv-executor.md` — **this very agent's own definition** — instructs: `uv run --directory ${CLAUDE_PLUGIN_ROOT} jerry ast frontmatter {deliverable_path}`, `jerry ast parse {deliverable_path}`, `jerry ast validate {deliverable_path} --schema {entity_type}`, none with `--quiet`, immediately followed by "Returns: {...}" — i.e. the calling convention explicitly documented in this framework assumes the entire captured output is parseable JSON.

**Plausibility:** Certain — this is not a hypothetical; it is the framework's current, shipped documentation and agent behavior, reproducible by grep.

**Consequence:** Once a `configured`-classification containment match occurs for any of these default (non-`--quiet`) invocations (which IN-001 shows is a realistic, even encouraged, configuration outcome), the R-4 transparency note prints to stderr on every single such invocation. Any harness that merges or naively concatenates stdout+stderr — explicitly named in the tournament's own C6 finding as `subprocess.run(capture_output=True) + naive concatenation`, which is a common pattern for agentic tool-calling frameworks — receives corrupted JSON exactly as the original C6 vulnerability described. The mitigation is real but is not reaching its own primary consumer by default.

**Evidence:** `skills/ast/SKILL.md` (grep for `--quiet`: zero matches); `skills/adversary/agents/adv-executor.md` lines 182, 187, 192 (no `--quiet` in any of the three documented `jerry ast` invocations); `parser.py`/`main.py` (`--quiet` default `False` on all 10 subcommands).

**Dimension:** Completeness (the fix's rollout to internal call sites is incomplete; the deliverable treats C6 as closed at the code layer without auditing consumers).

**Mitigation:** (a) Update `skills/ast/SKILL.md` to document `--quiet` and recommend it for all agent/programmatic (non-interactive) invocations. (b) Update `adv-executor.md` and any other Jerry-internal `.md` agent/skill definitions that invoke `jerry ast` expecting parseable stdout to add `--quiet`. (c) Consider a stronger default: auto-detect non-TTY stdout (or a `JERRY_AST_JSON_MODE` convention) and default `quiet=True` in that context, so JSON-consuming callers are safe without needing to remember an opt-in flag — inverting the current "safe only if you remember" posture to "safe by default."

**Acceptance Criteria:** Zero occurrences of `jerry ast <json-emitting-subcommand>` without `--quiet` in shipped Jerry skill/agent `.md` files; a regression test or lint check that flags new `jerry ast` invocations added to skill/agent definitions without `--quiet`.

---

### IN-003: Read-path TOCTOU retains the pre-fix structural gap; only the write path (`ast_modify`) was re-verified [MAJOR]

**Type:** Assumption
**Original Assumption:** C2's disposition ("Fixed") implies the TOCTOU class of vulnerability identified by the tournament is closed for `jerry ast` generally.

**Inversion:** What if an attacker (or racing process, in the same multi-tenant scenario IN-001 shows is realistic once shared-temp roots get configured) only needs to **read**, not write? `_check_path_containment` is called once inside `_read_file` (`ast_commands.py:309`), and its result feeds directly into `resolved.read_text()` (line 321) with no re-verification in between — the identical structural pattern the tournament flagged as unsafe for `ast_modify`'s write path, but never re-examined for the 9 other `ast_*` commands (`ast_parse`, `ast_render`, `ast_validate`, `ast_query`, `ast_frontmatter`, `ast_reinject`, `ast_detect`, `ast_sections`, `ast_metadata`) that only read. The write-time fix (`ast_commands.py:635`, TDD test #45) is real and well-designed, but it addresses one of ten call sites structurally exposed to the same class of race.

**Plausibility:** Medium — requires an attacker/racing process with write access to a directory that is itself inside an allowed containment root (the same precondition the tournament's own C3/C4 multi-tenant scenario already treats as in-scope), timed between the containment check and the subsequent read syscall.

**Consequence:** Content disclosure of a file outside all allowed containment roots via a successfully-raced symlink swap on a read-only command; unlike the write path, there is no mitigating "worst case is a no-op write" — the worst case here is data exfiltration via the `jerry ast` JSON output channel.

**Evidence:** `ast_commands.py:210-282` (`_check_path_containment`, no caller-side re-check contract), `:284-325` (`_read_file`, single check-then-read), `:634-638` (the *only* re-verification, scoped to `ast_modify`'s write); Section 3's C1-C6 table has no row for a read-path residual (contrast with the session-local config gap, which the plan *does* explicitly disclose as "a documented gap, not a silent omission" — the same transparency standard is not applied here).

**Dimension:** Internal Consistency (the plan's own stated discipline — "flagged transparently, not silently propagated" — is not applied uniformly across the deliverable).

**Mitigation:** Either (a) accept the read-path exposure explicitly as a documented, scoped residual risk (matching the plan's own transparency pattern used elsewhere), with rationale for why it's lower-priority than the write path, or (b) extend the same re-verification pattern used in `ast_modify` to `_read_file` itself (re-run `_check_path_containment` with `quiet=True` immediately before `resolved.read_text()`), closing the gap uniformly.

**Acceptance Criteria:** A TOCTOU PoC test analogous to test #45, but targeting a read-only command (e.g., `ast_parse`), either demonstrating rejection (if mitigated) or a documented, owner-signed-off risk acceptance (if not).

---

### IN-004: `get_project_root()`'s cwd/`CLAUDE_PROJECT_DIR` anchor is now trust-bearing, with no boundary search or drift detection [MAJOR]

**Type:** Assumption
**Original Assumption:** `get_project_root()` is marked "UNCHANGED" in Section 1's file-layout table, implying its existing resolution logic (`CLAUDE_PROJECT_DIR` env var, else cwd) remains adequate under the new design.

**Inversion:** What if the function's *risk profile* changed even though its *code* didn't? Previously, `get_project_root()` only decided where `jerry ast` looked for files to parse — a wrong answer meant "file not found." Under Option C, the same value now anchors `build_layered_config_adapter()`'s `root_config_path`/`project_config_path` (`project_root.py:85-112`), which determines **which `ast.trusted_roots` list is authoritative for this invocation**. There is no upward search (no `.git`/`pyproject.toml` boundary detection); if `CLAUDE_PROJECT_DIR` is unset (the expected condition for the plan's own stated **pip-package** deployment goal, since that env var is a Claude-Code-specific convention) and the tool is invoked from a nested subdirectory — a wrapper script, a CI job stage that `cd`s first, or simply a user running the pip-installed CLI from the wrong directory — `project_root` silently becomes that subdirectory. The resulting `.jerry/config.toml` lookup then either finds nothing (silently falling back to `[]` trusted roots — a fail-closed outcome, low risk) or, if that nested directory happens to contain its own `.jerry/config.toml` (e.g., a test fixture, an example project, or a nested untrusted checkout), silently honors a **different, potentially attacker-influenceable** trust configuration than the one the user believes is active.

**Plausibility:** Medium — requires an invocation context without `CLAUDE_PROJECT_DIR` and an unexpected cwd; explicitly more likely under the plan's own stated pip-extractability goal than under the Claude-Code-native usage pattern the rest of the design optimizes for.

**Consequence:** A silently-wrong trust grant — the user configured `ast.trusted_roots` correctly at the location they intended, but the running process reads a *different* file's config (or none), so the effective trust set diverges from what the user believes they configured, with zero warning (contrast with the R-3/R-4/relative-path warnings the design already added for other config-hygiene gaps).

**Evidence:** `project_root.py:40-54` (`get_project_root()`, no boundary search), `:85-112` (`build_layered_config_adapter()`, direct dependency on the unvalidated root); task framing's own stated requirement ("extractable as a pip package") as the condition under which `CLAUDE_PROJECT_DIR` is least likely to be set.

**Dimension:** Completeness (the design's threat modeling for config-source integrity covers `JERRY_PROJECT` traversal (AC-18, fixed) but not `project_root` drift, the more fundamental anchor both config paths derive from).

**Mitigation:** Add an upward boundary search (stop at the first ancestor containing `.git`, `pyproject.toml`, or an existing `.jerry/` directory) as a documented, tested resolution strategy for the no-`CLAUDE_PROJECT_DIR` case, or at minimum emit a one-line stderr note (mirroring the R-3/R-4/relative-path pattern already established) whenever `project_root` is resolved without `CLAUDE_PROJECT_DIR` and no `.jerry/config.toml` exists at that location, so an unexpected trust-config miss is never silent.

**Acceptance Criteria:** A test asserting that invoking `jerry ast` from a subdirectory without `CLAUDE_PROJECT_DIR` set either resolves to the correct ancestor project root or emits an explicit, testable warning.

---

## Recommendations

**Critical (MUST mitigate before merge):**
- IN-001-20260810T1500 — Extend broad-root detection to shared/multi-tenant OS temp shapes for `configured` roots; provide a safe, low-friction scratchpad-trust pattern that doesn't pressure users toward re-widening. Acceptance: broad-root warning fires for `/tmp`-class paths; documented scratchpad convention that avoids shared-ancestor configuration.
- IN-002-20260810T1500 — Update `skills/ast/SKILL.md` and all Jerry-internal agent/skill `.md` files (including `adv-executor.md`) that invoke `jerry ast` for JSON parsing to use `--quiet`; consider defaulting to quiet-when-non-TTY. Acceptance: zero unquiet JSON-emitting invocations in shipped `.md` files.

**Major (SHOULD mitigate):**
- IN-003-20260810T1500 — Either extend the write-time re-verification pattern to `_read_file`, or explicitly document the read-path TOCTOU exposure as a scoped, owner-accepted residual risk (per the plan's own transparency precedent). Acceptance: PoC test or documented risk acceptance.
- IN-004-20260810T1500 — Add boundary search or an explicit warning for `get_project_root()` resolution without `CLAUDE_PROJECT_DIR`. Acceptance: test covering the no-env-var, wrong-cwd scenario.

**Minor (MAY mitigate):**
- IN-005-20260810T1500 — Add an explicit "confirm `windows-latest` CI green" item to Section 7's sign-off checklist before merge (CI already covers this; the gap is process visibility, not code).
- IN-006-20260810T1500 — Reject or coerce-and-warn on non-string `ast.trusted_roots` entries and numeric/boolean-coerced single env values, consistent with the fail-closed precedent set for `JERRY_PROJECT` traversal.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | IN-002 (fix not propagated to canonical callers), IN-004 (project-root drift threat model gap) |
| Internal Consistency | 0.20 | Negative | IN-003 (transparency discipline applied to one gap, not another), IN-006 (fail-closed precedent applied inconsistently) |
| Methodological Rigor | 0.20 | Negative | IN-001 (broad-root threat model incomplete relative to the tournament's own established categories) |
| Evidence Quality | 0.15 | Negative | IN-005 (Windows claims rest on reasoning/mocking, not live execution — honestly disclosed, but unresolved at review time) |
| Actionability | 0.15 | Neutral | Every finding above has a concrete, testable mitigation and acceptance criterion |
| Traceability | 0.10 | Positive | Section 3's C1-C6 mapping and DD-1–DD-4 sign-off table make the deliverable's own residual-risk reasoning easy to cross-check against these findings |

**Overall assessment:** REVISE. The two Critical findings (IN-001, IN-002) both trace to the same pattern — a correct, well-reasoned code-level fix whose real-world safety depends on a downstream behavior (safe user configuration choices; consistent `--quiet` adoption) that the deliverable does not yet enforce, warn about, or audit for. Both are concretely evidenced against the actual shipped code and documentation, not speculative. The Major and Minor findings are narrower in scope and can reasonably proceed as tracked follow-ups with explicit disclosure, consistent with the transparency standard the plan itself sets for the session-local config gap.

---

*Prepared by adv-executor (blind S-013 execution, Group 5/6). Inputs: `eng-lead-option-c-plan.md`, direct reads of `containment_policy.py`, `project_root.py`, `ast_commands.py`, `parser.py`, `adapter.py`, `layered_config_adapter.py`, `env_config_adapter.py`, `red-vuln-option-c-findings.md` (context only, not a blind-round output), `skills/ast/SKILL.md`, `skills/adversary/agents/adv-executor.md`, `.github/workflows/ci.yml`. No source files modified. Persisted per P-002.*
