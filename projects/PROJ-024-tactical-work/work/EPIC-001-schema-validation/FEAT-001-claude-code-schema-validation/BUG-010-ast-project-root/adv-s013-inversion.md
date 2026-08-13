# Inversion Report: BUG-010 `jerry ast` Path Containment Scope Widening (PR #341)

**Strategy:** S-013 Inversion Technique
**Deliverable:** `src/interface/cli/{project_root,ast_commands,parser,main}.py` + tests, on branch `fix/BUG-010-ast-project-root`; plan artifacts `eng-lead-implementation-plan.md`, `red-vuln-findings.md`, `BUG-010-ast-project-root.md`
**Criticality:** C4 (tournament, Group E — blind executor)
**Date:** 2026-08-07
**Reviewer:** adv-executor (S-013 Inversion, blind background agent)
**H-16 Compliance:** This is a blind, isolated tournament agent (Group E: Structured Decomposition, per the 6-group order self-refine -> steelman -> challenge -> verify -> decompose -> score). The Steelman (S-003) group precedes this group in the tournament's declared ordering, but its output file was not provided to this execution and was not read. H-16 compliance is therefore **assumed satisfied by tournament sequencing, not directly confirmed** by this agent — flagged honestly per P-022 rather than fabricated.
**Goals Analyzed:** 7 (G1-G7) | **Assumptions Mapped:** 7 (A1-A7, 5 categories) | **Vulnerable Assumptions:** 7 (2 Major-code-level, 3 Major-design-level, 2 Minor)

---

## Summary

Systematic inversion of the BUG-010 scope-widening design surfaces one genuine, previously-undetected **code-level asymmetry** (IN-001: the `ast_modify` write-time TOCTOU recheck omits the H-01 ownership gate that the read-time check enforces, reopening the exact multi-tenant-corruption class the red-team remediation was meant to close) and three **design-level gaps** in how the additive-default containment model was chosen and documented (IN-002, IN-003, IN-004: the deny-by-default alternative was never evaluated on the record, the stderr-warning transparency mechanism assumes an attentive interactive user that a pip-package/CI future will not have, and no revisit trigger exists for when Jerry ships standalone). Recommendation: **REVISE** — fix IN-001 before merge (cheap, mirrors the existing read-path pattern); record the deny-by-default alternative's rejection rationale and a standalone-pip-package revisit trigger (IN-002/IN-004) as a documentation addition, not a blocking code change.

---

## Findings Table

| ID | Assumption / Anti-Goal | Type | Confidence | Severity | Evidence | Affected Dimension |
|----|------------------------|------|------------|----------|----------|--------------------|
| IN-001-20260807T-S013 | A5: threaded root/ownership logic stays consistent across all call sites | Assumption | Medium | **Major** | `ast_commands.py:677-682` (write-time recheck) vs. `:338-345` (read-time ownership gate) | Internal Consistency |
| IN-002-20260807T-S013 | A2/A3: single-user deployment model justifies default widening's risk/benefit trade | Assumption | Low | **Major** | `red-vuln-findings.md` L0 deployment-model table; BUG-010 entity Fix Approach (no revisit trigger) | Completeness / Traceability |
| IN-003-20260807T-S013 | A6: `--root` broad-root warning (R-3) reaches an attentive interactive user | Assumption | Medium | **Major** | `project_root.py:161-169` (`print(..., file=sys.stderr)`, non-blocking) | Evidence Quality |
| IN-004-20260807T-S013 | Anti-goal: deny-by-default alternative not evaluated on the record | Anti-Goal | N/A | **Major** | `eng-lead-implementation-plan.md` (no alternative-design section); `red-vuln-findings.md` (assesses given design only) | Methodological Rigor |
| IN-005-20260807T-S013 | A4: `st_uid`/`geteuid()` uniquely and reliably identifies "the current user" | Assumption | Medium | Minor | `ast_commands.py:280-287` (`_check_temp_root_ownership`) | Evidence Quality |
| IN-006-20260807T-S013 | A7: ad hoc root-list growth won't reintroduce IN-001-class drift | Assumption | Low | Minor | `project_root.py:171-177` (`get_containment_roots`); pattern that produced IN-001 | Methodological Rigor / Traceability |
| IN-007-20260807T-S013 | G1 anti-goal: containment re-anchors to Jerry's install tree | Anti-Goal | High (avoided) | N/A (strength) | `_get_repo_root()` retained but unused by containment logic (`ast_commands.py:160-178`) | — (positive evidence) |
| IN-008-20260807T-S013 | Minor: stderr transparency notes echo resolved paths to shared logs | Assumption | Low | Minor | `project_root.py:162-168`, `ast_commands.py:237-241` | Evidence Quality |

**Finding ID Format:** `IN-{NNN}-{execution_id}`, `execution_id = 20260807T-S013` (tournament Group E, blind executor, date 2026-08-07).

---

## Finding Details

### IN-001: Write-time TOCTOU recheck omits the H-01 ownership gate [MAJOR]

**Type:** Assumption (A5 — threaded logic stays consistent across all call sites)
**Original Assumption:** The plan and red-vuln both assert (and partially verify) that read-time and write-time containment "cannot disagree within one invocation" because both derive `allowed_roots` from the same `get_containment_roots(root)` call (eng-lead plan L1 File-by-File Plan §2, "ast_modify write-time TOCTOU recheck"; red-vuln H-05 "reusing the same `root` param as the read call").
**Inversion:** That claim is true for the **containment-roots** predicate but false for the **ownership** predicate layered on top by the H-01 remediation. `_check_path_containment()` (called only from `_read_file`, hence only at read time) runs `_is_temp_default_root_match()` -> `_check_temp_root_ownership()` before returning success (`ast_commands.py:338-345`). `ast_modify`'s write-time recheck (`ast_commands.py:677-682`) is a **separate, inline** block that calls `get_containment_roots(root)` and checks `target_path.is_relative_to(r)` only — it never calls `_check_temp_root_ownership` or `_is_temp_default_root_match`.
**Plausibility:** High. This is not a hypothetical — it is directly observable by reading the two code blocks side by side; no exploit was run, but the code asymmetry itself is a verified fact, not an inference.
**Consequence:** `target_path = Path(file_path).resolve()` is recomputed independently at write time (a second, separate `.resolve()` call from the one inside the read-time `_check_path_containment`). If an attacker with write access to a shared temp root (the same multi-tenant `/tmp`/`gettempdir()` scenario H-01 was written to close) retargets a symlink at `file_path` between the read-time check succeeding and the write-time `os.replace()` executing, the write-time recheck will follow the new symlink to a **different real file**, verify only that it falls under an allowed root (true — it is still inside the same temp root), and then `os.replace()` the attacker-chosen destination directly — with **zero ownership verification** at the moment that matters most (the actual write). This precisely reopens the CWE-552/CWE-668/CWE-281 class the H-01 remediation was built to close, for the one command (`ast_modify`) that actually mutates files. Severity is bounded (narrow TOCTOU race window, requires attacker write access to the same shared temp directory — the same precondition already accepted as elevated-risk for H-01) but the gap is real, unmitigated, and untested (no test in `test_ast_commands.py` exercises an ownership mismatch introduced between read and write).
**Evidence:** `src/interface/cli/ast_commands.py:677-682` (write-time recheck, no ownership call) vs. `:338-345` (read-time ownership gate, only reachable via `_read_file` -> `_check_path_containment`).
**Dimension:** Internal Consistency (the deliverable's own stated invariant — "no window where read and write disagree" — does not hold for the ownership dimension it was extended to cover).
**Mitigation:** Replace the write-time recheck's inline `get_containment_roots` + `is_relative_to` logic with a call to the same `_check_path_containment(file_path, root)` function used at read time (or, if the TOCTOU-recheck-on-the-resolved-path semantics must differ slightly, explicitly call `_check_temp_root_ownership(target_path, file_path)` immediately after the existing root-containment check, gated by the same `_is_temp_default_root_match` predicate). This is a small, low-risk change that reuses existing, already-tested logic rather than introducing new code.
**Acceptance Criteria:** A new test (e.g., `test_ast_modify_when_write_target_ownership_changes_between_read_and_write_then_rejected`) that simulates an ownership mismatch surfacing only at write time (via `monkeypatch` on `os.geteuid` or on the target's `st_uid` between the read and write phases of a single `ast_modify` call) asserts the write is rejected with a descriptive error, not silently completed.

---

### IN-002: Default-widening's risk/benefit trade is justified against today's deployment model with no revisit trigger for tomorrow's [MAJOR]

**Type:** Assumption (A2 combined with A3)
**Original Assumption:** "The convenience benefit of auto-allowing OS temp/scratchpad directories by default outweighs the security cost, because Jerry's current dominant deployment is a single-user dev laptop / Claude Code plugin" (red-vuln L0: "Jerry's primary distribution today is a single-developer CLI/plugin run on a personal machine").
**Inversion:** Invert the assumption: "Jerry's deployment model changes (standalone pip package, CI runners, shared/multi-tenant hosts) and the default-widening's risk profile silently escalates from MEDIUM to HIGH with no code or process change required to trigger re-evaluation." This is not a remote hypothetical — the BUG-010 entity's own framing (and the task instructions this review was executed under) explicitly names "the standalone-pip-package future" as a stated, anticipated direction for Jerry, distinct from the Claude Code plugin context the temp-root default was designed for.
**Plausibility:** Medium-High. Nothing in the code, the eng-lead plan, or the BUG-010 entity ties the temp-root default's justification to a runtime signal (e.g., detecting whether `CLAUDE_PROJECT_DIR` or another Claude-Code-specific marker is present) or to a documented revisit condition. The default is unconditional: every invocation of `jerry ast`, regardless of caller or environment, gets the widened temp-root allowance.
**Consequence:** If/when Jerry ships as a standalone pip package invoked in CI pipelines, containers, or shared build hosts — contexts where `/tmp` and `gettempdir()` are far more likely to be genuinely multi-tenant than "a personal machine" — the security posture degrades from the accepted MEDIUM to the already-identified HIGH (per red-vuln's own table) **silently**, because nothing in the design links the default's justification to the deployment context it was justified against.
**Evidence:** `red-vuln-findings.md` L0 deployment-model disclosure table (lines ~81-87); `eng-lead-implementation-plan.md` L1 Risks (R-1: "Accepted, owner-approved risk... not open" — accepted as a static policy, not a conditional one); no `CLAUDE_PROJECT_DIR`-gating or equivalent runtime-context check exists anywhere in `project_root.py`'s `get_containment_roots()`.
**Dimension:** Completeness (the deliverable's risk acceptance is scoped to one deployment model without acknowledging the other named future one) / Traceability (no tracked follow-up item ties the "standalone pip package" future to a containment-default re-evaluation).
**Mitigation:** See [Recommendations: Design Alternative DR-2](#design-alternative-dr-2-context-gated-default-widening) below. At minimum: record in the BUG-010 entity or a short ADR that (a) the deny-by-default alternative was considered and rejected for the reason X, and (b) a revisit trigger exists ("when `jerry` is distributed via PyPI/standalone install outside the Claude Code plugin context, re-evaluate whether temp-root default-inclusion should be gated behind Claude-Code-context detection").
**Acceptance Criteria:** BUG-010 entity's `## Fix Approach` or a linked ADR contains an explicit "Alternatives Considered" note addressing the deny-by-default design and a stated revisit condition tied to standalone-distribution.

---

### IN-003: Broad-root stderr warning (R-3) assumes an attentive interactive human [MAJOR]

**Type:** Assumption (A6)
**Original Assumption:** `--root` is "the user's discretion... It's at the user's discretion to approve the use of the command." The R-3 mitigation (stderr WARNING for filesystem-root/home-ancestor `--root` values) operationalizes this as: the tool warns, the user reads the warning, and decides whether to proceed.
**Inversion:** "What if there is no human reading stderr at the moment the warning is printed?" This is not implausible — it is the **normal** operating mode for a standalone pip-installed CLI tool run from a script, a CI job, or a cron task, none of which is Claude Code's interactive scratchpad workflow this design was built around. In such contexts, stderr is commonly redirected (`2>/dev/null`), captured into a log file nobody reviews synchronously, or simply not surfaced to any human before the (already-completed, non-blocking) operation finishes.
**Plausibility:** High for the "standalone pip package" future explicitly named in this review's scope; Low-Medium for Jerry's current Claude-Code-plugin-dominant usage (where an agent or the user is more likely to observe tool output, though even there, sub-agent tool output is not guaranteed to be read carefully by a human before further automated action).
**Consequence:** The entire R-3 control (the only defense against `--root /`-class maximally-broad overrides) degrades from "advisory but effective" to "silently ineffective" precisely in the deployment context (non-interactive/CI/scripted) where a broad, mistaken, or malicious `--root` value is most consequential and least likely to be caught by a human before damage occurs.
**Evidence:** `project_root.py:161-169` — the warning is `print(..., file=sys.stderr)` only; no exit-code change, no confirmation prompt, no distinction between interactive (`sys.stdin.isatty()`) and non-interactive invocation.
**Dimension:** Evidence Quality (the control's effectiveness claim — "best-effort protection" — is not qualified by the invocation context it depends on).
**Mitigation:** Document the residual gap explicitly (cheapest option — MAY): add a line to `get_containment_roots`'s docstring and to the BUG-010 entity noting that R-3 is advisory-only and provides no protection in non-interactive/automated invocations. Optionally (SHOULD, not required to close this finding): consider whether a broad `--root` combined with a non-tty stdin should be treated more strictly in a future iteration — flagged as a forward-looking recommendation, not a blocking requirement for this PR, consistent with how R-3/R-4 were themselves treated as owner-confirmable open decisions in the eng-lead plan.
**Acceptance Criteria:** Docstring/entity documentation update acknowledging the non-interactive gap explicitly (minimum bar); no code change required to close this finding at Major-documentation level.

---

### IN-004: The deny-by-default (`--root` required for all non-project access) alternative was never evaluated on the record [MAJOR]

**Type:** Anti-Goal (methodological completeness)
**Inversion of the design goal:** "What would guarantee this deliverable fails to demonstrate it chose the right design?" Answer: implement the owner's directive literally, without ever writing down — anywhere in the eng-lead plan, the red-vuln findings, or the BUG-010 entity — the more conservative alternative that was available and its rejection rationale. That is exactly what happened here.
**Alternative Design (fully specified per task instruction (a)):** Do not widen the *default* allowed-roots set at all. Keep the default at "project root only" (the original PR #341 scope). Require every access outside the project root — including Claude Code scratchpad writes — to go through the existing `--root <path>` exclusive-override flag.
**Trade-off analysis:**

| Dimension | Current design (additive default + `--root` override) | Alternative (deny-by-default, `--root` required for all external access) |
|---|---|---|
| Security surface | Widened by default for every invocation, regardless of caller; H-01 ownership gate needed as a compensating control (and, per IN-001, is incompletely applied) | Zero default widening; no H-01 exposure class exists at all — nothing to gate |
| Code/test complexity | `_is_temp_default_root_match`, `_warn_if_temp_root_match`, `_check_temp_root_ownership`, `_HARDCODED_TMP` seam, ~20 dedicated tests (T-1/T-2/T-3) | None of the above needed; `get_containment_roots` collapses to project-root-or-explicit-root, matching the original (pre-widening) PR #341 shape |
| Scratchpad ergonomics | Works with zero extra flags from any caller (agent, skill, human) | Every caller (skills, agents, wrapper scripts) must remember to pass `--root <scratchpad-dir>`; a caller that forgets it gets a hard failure instead of silent success — shifts a security decision onto N call sites instead of one central function |
| Failure mode if forgotten | N/A (no flag to forget for the scratchpad case) | Silent-looking failure ("Path escapes allowed containment roots") for legitimate scratchpad use until every caller is updated — real regression risk during rollout, and a incentive for callers to reach for an overly broad `--root` (e.g., always passing `--root /tmp`) to make the error go away, which is arguably a worse outcome than the current ownership-gated default |
| Fit for standalone-pip-package future | Directly appropriate — a general-purpose CLI tool with no Claude-Code-specific knowledge should not implicitly trust OS temp directories by default | Also appropriate, but at the cost of scratchpad ergonomics that matter specifically to the Claude-Code-plugin use case |

**Assessment:** The alternative is genuinely simpler and safer in the abstract (fewer moving parts, no IN-001-class asymmetry possible because there is no implicit temp-root code path to have an asymmetry in), but it is not a strict improvement — it trades a code-level security gap for a rollout/ergonomics regression risk that could itself produce worse security outcomes (callers reflexively widening `--root` to make failures go away) if not paired with disciplined caller updates across every skill/agent that shells out to `jerry ast`. **Neither this review nor the eng-lead plan can responsibly declare a winner without knowing how many call sites (skills, agents, hooks) currently rely on the implicit temp-root default** — that inventory was not performed by any of the artifacts reviewed here.
**Evidence:** Absence — no section of `eng-lead-implementation-plan.md` or `red-vuln-findings.md` performs this trade-off analysis or names the deny-by-default alternative; both proceed directly from the owner's directive to implementation/verification of the chosen design.
**Dimension:** Methodological Rigor (S-013's mandate is exactly to surface this class of un-evaluated alternative).
**Mitigation:** Record the trade-off table above (or an equivalent) in the BUG-010 entity as a documented "Alternatives Considered" note, with the owner's directive cited as the deciding rationale (which is a legitimate, sufficient rationale — the gap is that it is not written down, not that the decision itself was wrong).
**Acceptance Criteria:** BUG-010 entity contains a short "Alternatives Considered" subsection under `## Fix Approach` naming the deny-by-default alternative and its rejection rationale.

---

## Recommendations

**MUST mitigate (Major, code-level):**
- **IN-001-20260807T-S013** — Route the `ast_modify` write-time recheck through the same ownership-gated path used at read time (reuse `_check_path_containment` or explicitly call `_check_temp_root_ownership`). Acceptance: dedicated ownership-mismatch-between-read-and-write regression test passes.

**SHOULD mitigate (Major, design/documentation-level):**
- **IN-002-20260807T-S013** — Record a revisit trigger tied to the standalone-pip-package future in the BUG-010 entity or a linked ADR.
- **IN-003-20260807T-S013** — Document the non-interactive/CI gap in R-3's advisory-only warning explicitly.
- **IN-004-20260807T-S013** — Record the deny-by-default alternative and its rejection rationale as an "Alternatives Considered" note (see [Design Alternative DR-2](#design-alternative-dr-2-context-gated-default-widening) for the recommended synthesis).

**MAY mitigate (Minor):**
- **IN-005-20260807T-S013** — Note the container/UID-namespace edge case for the ownership check as a known limitation.
- **IN-006-20260807T-S013** — Consider refactoring the ad hoc root list into a small `(path, requires_ownership_check, is_explicit)` structure before a third scratchpad-style root is added, to prevent IN-001-class drift from recurring.
- **IN-008-20260807T-S013** — No action required; noted for completeness.

### Design Alternative DR-2: Context-gated default widening

The strongest synthesis of task items (a) and (c) is **not** a binary choice between "widen by default" and "require `--root` for everything," but a **third option neither the eng-lead plan nor red-vuln evaluated**: gate the temp/scratchpad default-inclusion behind detection of the Claude-Code-plugin runtime context, using the same signal `get_project_root()` already checks (`CLAUDE_PROJECT_DIR` presence):

- **When `CLAUDE_PROJECT_DIR` (or another Claude-Code-specific marker) is present:** current behavior — project root + temp/scratchpad defaults, ownership-gated. This is the context the scratchpad ergonomics genuinely matter for.
- **When absent (standalone pip-installed CLI, CI, generic script invocation):** default to project-root-only, matching the more conservative posture appropriate for a general-purpose tool with no Claude-Code-specific knowledge of what a "scratchpad" even is. `--root` remains available as the explicit override in both contexts, unchanged.

This directly resolves IN-002 (the risk/benefit trade becomes conditional on the deployment signal that actually determines which model applies, rather than a static global default) and substantially narrows IN-004's alternative-design gap (it captures the ergonomic benefit of the current design in the context it was built for, while adopting the safer posture of the deny-by-default alternative for every other context) without requiring every skill/agent caller to be individually audited and updated to pass `--root` (the main rollout risk identified against the pure deny-by-default alternative). It does **not** address IN-001, which is a code-level bug independent of which default-widening policy is chosen and MUST be fixed regardless of which design direction is taken.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | IN-002: risk acceptance scoped to one deployment model, silent on the other named future one; IN-001: AC list does not cover write-time ownership consistency |
| Internal Consistency | 0.20 | Negative | IN-001: the deliverable's own stated invariant ("read/write cannot disagree") is false for the ownership predicate specifically |
| Methodological Rigor | 0.20 | Negative | IN-004: deny-by-default alternative never evaluated or recorded; IN-006: no per-root policy abstraction to prevent IN-001-class recurrence |
| Evidence Quality | 0.15 | Negative | IN-003: R-3's "best-effort protection" claim unqualified by non-interactive-invocation context; IN-005: container/UID edge case unaddressed |
| Actionability | 0.15 | Neutral-Positive | Existing AC items are concrete and testable; this report's own mitigations (IN-001 especially) are equally concrete, small, and reuse existing tested code paths |
| Traceability | 0.10 | Negative | IN-002: no tracked follow-up item links the stated "standalone pip package" future to a containment-default re-evaluation trigger |

**Overall assessment:** REVISE. IN-001 is a genuine, narrow-but-real code gap that should block merge until fixed (cheap fix, mirrors existing tested pattern). IN-002/IN-003/IN-004 are documentation/design-completeness gaps that do not block merge but should be recorded before this scope-widening is considered closed, especially given the deliverable's own stated forward intent toward a standalone pip-package distribution model.

---

*S-013 Inversion execution complete. Blind executor (Group E), no access to other strategies' findings in this tournament round. Assessment only — no source files modified.*
