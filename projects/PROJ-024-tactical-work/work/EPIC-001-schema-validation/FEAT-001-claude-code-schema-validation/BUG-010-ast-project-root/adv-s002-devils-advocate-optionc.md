# Devil's Advocate Report: BUG-010 Option C — `jerry ast` Containment Redesign (User-Declared Trusted Roots)

**Strategy:** S-002 Devil's Advocate
**Deliverable:** `eng-lead-option-c-plan.md` + implementation (`src/interface/cli/containment_policy.py`, `project_root.py`, `ast_commands.py`, `parser.py`/`main.py`/`adapter.py`) @ branch `fix/BUG-010-ast-project-root` `cce557c5`
**Criticality:** C4 (blind tournament group; AE-005 security-relevant)
**Date:** 2026-08-10
**Reviewer:** adv-executor (blind, Group 3 of 6: Challenge)
**H-16 Compliance:** S-003 Steelman applied by adv-executor (blind, Group 2 of 6), persisted at `adv-s003-steelman-optionc.md` (confirmed — 7 improvement findings, recommendation: "Ready for downstream critique strategies")

---

## Summary

7 counter-arguments identified (2 Critical, 3 Major, 2 Minor). The deliverable's implementation-level correctness is well-evidenced (red-vuln's independent 21-case re-check corroborates it), but the *design's core trust assumptions* have two fundamental gaps: (1) "trust = explicit user declaration" silently conflates "user" with "the LLM agent operating the tool" in Jerry's actual dominant deployment context, letting the contained party self-widen its own containment through a channel it can already write to (DA-001), and (2) the highest-precedence trust channel (`JERRY_AST__TRUSTED_ROOTS` env var) is exactly the kind of externally-influenceable input the design already treats as attacker-adjacent for `JERRY_PROJECT` (AC-18) but never applies the same scrutiny to for the trust declaration itself (DA-002). Recommend REVISE: the Critical findings do not invalidate Option C's core thesis (declared trust over implicit auto-widen remains correct), but they do invalidate the plan's implicit assumption that "user-declared" is a sufficient security predicate on its own, without also constraining *who/what* can write the declaration.

---

## Findings Table

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| DA-001-20260810T0900 | "Explicit user grant" trust model conflates "user" with "agent"; the contained party can self-widen its own containment persistently | Critical | `eng-lead-option-c-plan.md` L38-45 (mandate); `adv-s003-steelman-optionc.md` SM-001 best-case condition (L44); `.gitignore` L63-64 (`.jerry/` untracked, filesystem-writable) | Methodological Rigor |
| DA-002-20260810T0900 | Env var sits at the HIGHEST trust precedence tier with no scrutiny applied to *who controls the CLI's environment*, despite the design applying exactly this scrutiny to `JERRY_PROJECT` (AC-18) | Critical | `eng-lead-option-c-plan.md` L238 (precedence table); `red-vuln-option-c-findings.md` AC-7 (L102-105), AC-18 (L179-188, MEDIUM finding on a structurally identical channel) | Completeness |
| DA-003-20260810T0900 | DD-2's "remove ownership gate entirely" argument dismisses the persistence/durability of `configured` roots as "merely quantitative," but durability is exactly why a defense-in-depth check matters more, not less | Major | `eng-lead-option-c-plan.md` L500 (DD-2); `adv-s003-steelman-optionc.md` SM-001 (L38-44) | Methodological Rigor |
| DA-004-20260810T0900 | Warn-and-honor on relative `ast.trusted_roots` entries assumes a human reads stderr; the dominant invocation pattern (agent subprocess calls, `--quiet` available) makes the "warn" half unobserved in practice | Major | `project_root.py` L214-222; `adv-s003-steelman-optionc.md` SM-004 (L74-80); `eng-lead-option-c-plan.md` L308 (C6 `--quiet` disposition) | Actionability |
| DA-005-20260810T0900 | No least-privilege ratchet across config layers — project-scoped config can declare broader `ast.trusted_roots` than root/framework config with no enforced subset relationship | Major | `eng-lead-option-c-plan.md` L238 (precedence: project overrides root); `project_root.py` L88-105 (`build_layered_config_adapter`) | Completeness |
| DA-006-20260810T0900 | DD-3's hard-coded `quiet=True` write-time suppression deduplicates the transparency note at exactly the highest-stakes moment (the mutation), not the lower-stakes read | Minor | `eng-lead-option-c-plan.md` L190-197 (write-time recheck), L501 (DD-3 rationale) | Internal Consistency |
| DA-007-20260810T0900 | `--root`'s full exclusivity (excludes project root, not additive) creates a usability incentive toward habitually broad `--root` values to avoid losing project access, which the design does not examine | Minor | `containment_policy.py` L120-124, L143-150 (explicit-root branch); `RESUME-HERE.md` L32 | Actionability |

**Finding ID Format:** `DA-{NNN}-{execution_id}` where `execution_id = 20260810T0900`.

---

## Finding Details

### DA-001: The "Explicit User Grant" Model Conflates "User" With "Agent" [CRITICAL]

**Claim Challenged:** The plan's core thesis (L38-45) and its steelman reconstruction both rest on the premise that `ast.trusted_roots` entries are a deliberate, legible act by a trustworthy principal. SM-001's own stated best-case condition makes this explicit: *"the config file(s) supplying `ast.trusted_roots` are themselves subject to the same access control as the rest of the user's repository/environment (i.e., an attacker who can write `.jerry/config.toml` already has write access equivalent to or exceeding what `ast.trusted_roots` would grant)."*

**Counter-Argument:** That best-case condition silently equates "an attacker" with "the party being contained" and dismisses the case as trivial ("they already have write access, so what does it matter"). But the entity `jerry ast` containment exists to constrain is not primarily an *external attacker* — per `RESUME-HERE.md` and the plan's own repeated references to "agent scratchpad ops" and Claude Code's `CLAUDE_PROJECT_DIR` mechanism, the actual operative threat model this control was built for is **an LLM agent operating semi-autonomously inside the repository via tool calls**, where containment is meant to bound the *blast radius of the agent's own actions*, not (only) to stop a human attacker who has already compromised the machine. An agent with ordinary Write-tool access — the same access level the agent already has to write `.jerry/config.toml` — can add its own scratchpad or working directory to `ast.trusted_roots` in one write, and that grant then persists across every subsequent `jerry ast` invocation for the rest of the session (and future sessions, since `.jerry/config.toml` is a durable file). This is qualitatively different from "the attacker already had write access": it converts a *momentary, reviewable* act (writing a file the agent was already going to write) into a *durable, silent expansion* of exactly the control meant to bound what the agent can subsequently read/write through `jerry ast` specifically — a control whose entire value proposition, per the L0 mandate, is auditability ("a security reviewer can now answer 'what does `jerry ast` trust?' by running `jerry config get ast.trusted_roots`" — but nothing prevents the answer from having been written by the same agent whose trust is in question, between two reviews).

**Evidence:** `eng-lead-option-c-plan.md` L27-32 ("No directory is trusted unless the project owns it or the user explicitly configured it" — no distinction drawn between "user" and "agent acting as the user's proxy"); `.gitignore` L63-64 confirms `.jerry/` and `projects/*/.jerry/` are untracked (filesystem-writable, not subject to PR review even in principle); `adv-s003-steelman-optionc.md` L44 (the steelman's own stated best-case condition, which this finding directly attacks).

**Impact:** If valid, the containment redesign's core security property ("no directory is trusted unless... the user explicitly configured it") does not hold against the deployment context the tool is actually built for. An agent that drifts, is prompt-injected, or simply misapplies its own judgment can silently and durably widen its own leash with no distinct signal beyond a config diff nobody is guaranteed to review before the next invocation reads it.

**Dimension:** Methodological Rigor

**Response Required:** The creator must either (a) demonstrate that the deployment model genuinely is single-tenant-human-only for the `ast.trusted_roots` write path specifically (e.g., because Claude Code's tool-permission layer independently gates writes to `.jerry/config.toml` separately from ordinary file writes — if such a gate exists, cite it), or (b) revise the design to treat a write to `ast.trusted_roots` itself as a privileged, reviewable action distinct from ordinary file writes (e.g., require the entry to also be explicitly acknowledged via a separate `--root`-style CLI flag or an explicit human-confirmation step the first time each entry is used), or (c) explicitly document this as an accepted residual risk with the specific deployment assumption stated (not merely implied via a steelman's best-case condition).

**Acceptance Criteria:** A new subsection in Section 7 (or a DD-5) that states explicitly whether an agent's own file-write capability is assumed to be sufficient authorization to expand its own containment, with the rationale for why that assumption is safe in Jerry's actual agent-in-the-loop deployment model — not merely asserted via the single-tenant-CLI framing carried over from `--root`'s pre-existing, narrower (single-invocation, non-persistent) precedent.

---

### DA-002: Env-Var Precedence Is the Highest-Trust Channel With No Applied Scrutiny [CRITICAL]

**Claim Challenged:** The config contract (L238) states precedence as ENV (`JERRY_AST__TRUSTED_ROOTS`) > Project config > Root config > Default `[]` — env wins over everything, including the user's own persisted file-based declarations.

**Counter-Argument:** The design already recognizes, for a structurally near-identical channel, that an externally-influenceable input reaching a trust-relevant config path is a genuine security finding: AC-18 (confirmed MEDIUM by red-vuln) is exactly "an environment variable (`JERRY_PROJECT`) that something other than the interactive user may set steers a trust-relevant config read." But `JERRY_AST__TRUSTED_ROOTS` is the *same class of input* — a process environment variable — sitting at the *highest* precedence tier for the trust declaration itself, not merely for which file gets read. Nowhere in Section 2, Section 3, or Section 7 does the plan ask "who sets the environment `jerry ast` runs in, and is that set of parties as trustworthy as the user editing `.jerry/config.toml` by hand?" In Jerry's actual usage (Claude Code plugin/subprocess invocation, CI runners, wrapper scripts, potentially MCP-server-mediated tool calls), the process environment is frequently constructed by an orchestration layer the interactive human user does not directly control turn-by-turn — a compromised or misconfigured wrapper, a templated CI job, or an MCP server relaying environment variables could inject or override `JERRY_AST__TRUSTED_ROOTS` without ever touching the repository's `.jerry/config.toml` at all, and would silently *out-rank* whatever the user had actually declared in that file. red-vuln's AC-7/AC-8/AC-9 tested only whether env-value *parsing* is correct (mis-forms fail safe, values parse as declared) — they did not test, because it was out of red-team's scope (implementation correctness of an accepted design, not design acceptance itself), whether ENV *should* be the highest-precedence source for a security boundary declaration in the first place.

**Evidence:** `eng-lead-option-c-plan.md` L238 (precedence table, ENV ranked #1); `red-vuln-option-c-findings.md` L179-188 (AC-18, confirmed MEDIUM finding on the structurally analogous `JERRY_PROJECT` channel, explicitly scoped to "shared/multi-tenant host" deployment models as the realistic exploitation context — the same deployment models where an untrusted or semi-trusted process could plausibly control the invocation environment of a `jerry ast` subprocess); `red-vuln-option-c-findings.md` L102-115 (AC-7/AC-8/AC-9, confirming correctness of the mechanism but never challenging whether the mechanism's precedence ordering is the right security posture).

**Impact:** If a deployment context exists where the process environment is set by a less-trusted party than the one who authored `.jerry/config.toml` (the same "shared/multi-tenant" model AC-18 already flags as realistic for CI), that party can override the user's file-declared trust boundary entirely, silently, without leaving any artifact in the repository at all — a strictly stealthier vector than the already-confirmed AC-18 finding, because AC-18 at least requires a pre-positioned file on disk, whereas an env-var override requires nothing but control of the subprocess environment.

**Dimension:** Completeness

**Response Required:** The creator must either (a) provide an explicit threat-model justification for why env-var precedence is safe for this specific security-relevant key even though the same environment-control concern was found MEDIUM-severity for `JERRY_PROJECT`, (b) demonstrate that the deployment models where `JERRY_PROJECT`-via-environment is realistic (CI/shared hosts) are categorically different from where `JERRY_AST__TRUSTED_ROOTS`-via-environment is realistic, or (c) revise the precedence model for this specific key (e.g., exclude `ast.trusted_roots` from env-var override entirely, or require the env-supplied value to be a subset of the file-declared value rather than an outright override).

**Acceptance Criteria:** A new subsection (or DD-5) explicitly addressing whether `JERRY_AST__TRUSTED_ROOTS`'s env-precedence position was a deliberate security decision or an unexamined consequence of reusing `LayeredConfigAdapter`'s generic precedence model as-is for a security-relevant key. If deliberate, cite the rationale; if unexamined, propose and evaluate at least one alternative precedence model for this key specifically.

---

### DA-003: DD-2's Ownership-Gate Removal Dismisses Persistence as "Merely Quantitative" [MAJOR]

**Claim Challenged:** SM-001 (adopted verbatim as the strengthened rationale for DD-2, per the steelman) states: *"`--root`... and `ast.trusted_roots` entries... are the SAME trust primitive — EXPLICIT USER GRANT — differing only in cardinality (one vs. many) and persistence (single invocation vs. durable config)."* This framing is used to conclude that because `--root` never had an ownership gate, `configured` roots do not need one either.

**Counter-Argument:** Treating persistence as a mere accounting difference ("cardinality... and persistence") rather than the central variable is precisely backwards for evaluating whether an ownership/integrity check adds value. An ownership gate's entire purpose is to catch a *drift* condition: a directory that was safe to trust at declaration time but has since become unsafe (e.g., a shared NFS/network mount's ownership changes, a symlink target is repointed by another process on a shared host, a directory is later repurposed). `--root`'s ephemerality makes such drift largely moot — the user re-asserts trust fresh, in-band, every single invocation, so there is no window for conditions to have silently changed since the last trust assertion. `ast.trusted_roots`'s durability is exactly the opposite: an entry declared once can remain trusted for weeks or months without the user ever re-examining whether the underlying directory's ownership or shared-access characteristics still match the conditions that made the original grant safe. DD-2's own fallback text (L500) *already acknowledges this exact scenario* — "a `configured` root could still be a genuinely shared directory the user trusts but doesn't fully control write-ownership within" — yet the default recommendation (Section 7, DD-2, "Remove entirely") does not treat this as the primary case to design for; it treats it as an optional fallback for an owner who "prefers defense-in-depth," implying the default posture is that this scenario is unlikely enough to not warrant the check by default. The plan supplies no evidence (usage data, deployment survey, or even a stated assumption) for why durable, unaudited config-declared trust is less likely to encounter ownership drift than the ephemeral `--root` case it is equated with.

**Evidence:** `eng-lead-option-c-plan.md` L500 (DD-2 rationale and fallback text); `adv-s003-steelman-optionc.md` L38-44 (SM-001, the unification argument this finding directly rebuts).

**Impact:** If the ownership gate is removed entirely as recommended, a `configured` root whose ownership characteristics change after declaration (the scenario DD-2's own text concedes is plausible) has zero remaining check — not "reduced," zero. The persistence that makes this scenario realistic is the same persistence the unification argument treats as a reason the check is unnecessary.

**Dimension:** Methodological Rigor

**Response Required:** The creator must either (a) provide affirmative evidence or a stated assumption for why ownership drift on durable `configured` roots is sufficiently unlikely in Jerry's actual deployment model to justify defaulting to "remove entirely" rather than "retain fail-closed, scoped to `configured`," or (b) change the DD-2 default recommendation to the fail-closed, `configured`-scoped variant the plan itself already specifies as a fully-designed fallback (L500), making it the primary recommendation rather than an opt-in alternative.

**Acceptance Criteria:** DD-2 either gains an explicit "durability changes the risk calculus versus `--root`" analysis justifying the current default, or the default flips to the fail-closed scoped-ownership-check variant that the plan's own fallback text already fully specifies (no new design work required — only a change in which branch is the default).

---

## Recommendations

**P0 (Critical — MUST resolve before acceptance):**
- **DA-001:** Add an explicit design statement addressing whether an agent's own Write-tool capability is treated as sufficient authorization to durably expand `jerry ast`'s own containment via `.jerry/config.toml`, and why that is safe (or a mitigation) in Jerry's actual agent-in-the-loop deployment model. Acceptance criteria: new subsection with explicit rationale, not an inherited best-case condition from the steelman.
- **DA-002:** Justify or revise `JERRY_AST__TRUSTED_ROOTS`'s highest-precedence position given the design's own AC-18 precedent that environment-influenced trust-relevant paths are a confirmed finding class. Acceptance criteria: explicit threat-model justification citing why this key's env-precedence is safe despite the structurally analogous `JERRY_PROJECT` finding, or a precedence-model revision for this specific key.

**P1 (Major — SHOULD resolve; require justification if not):**
- **DA-003:** Either justify why ownership drift on durable `configured` roots is unlikely enough to default to full gate removal, or flip DD-2's default to the fail-closed, `configured`-scoped variant already specified in the plan's own fallback text.
- **DA-004:** Reassess the "warn-and-honor" rationale (SM-004) against the actual dominant invocation pattern (automated/agent subprocess calls where stderr may not be parsed and `--quiet` is available) — either add a machine-readable signal (e.g., a structured warning in JSON output, not only stderr text) or accept and document that the practical effect for non-human consumers is "silently honor."
- **DA-005:** Add an explicit least-privilege constraint across config layers — e.g., document (or enforce) that project-scoped `ast.trusted_roots` entries should not silently exceed the scope a security-conscious root/framework-level config intended, or explicitly accept the absence of this constraint with rationale.

**P2 (Minor — MAY resolve; acknowledgment sufficient):**
- **DA-006:** Acknowledge that DD-3's write-time note suppression removes the transparency signal at the highest-stakes moment (the mutation) rather than the read; consider a distinct (even if terser) write-time signal instead of full suppression.
- **DA-007:** Acknowledge the usability-incentive risk that `--root`'s full exclusivity (vs. additive) could push users/agents toward habitually broad `--root` values to avoid losing project-root access.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | DA-002, DA-005: the design does not examine the env-precedence trust channel's exposure or cross-layer least-privilege, despite examining structurally similar channels (`JERRY_PROJECT`) elsewhere in the same document |
| Internal Consistency | 0.20 | Negative | DA-006: the design's own stated transparency goal (visibility into what `jerry ast` trusts) is undercut by DD-3's write-time suppression at the highest-stakes moment |
| Methodological Rigor | 0.20 | Negative | DA-001, DA-003: the core trust-model justification (SM-001's unification principle) elides the "user vs. agent" distinction and treats persistence as incidental rather than central to the ownership-gate removal decision |
| Evidence Quality | 0.15 | Neutral | Implementation-level claims are exceptionally well-evidenced (red-vuln's independent 21-case re-check); the gaps found here are in unexamined design assumptions, not unsupported implementation claims |
| Actionability | 0.15 | Negative | DA-004, DA-007: "warn-and-honor" and "--root exclusivity" both carry practical-effectiveness or usability-incentive gaps not addressed by the plan's stated response (documentation/warning only) |
| Traceability | 0.10 | Neutral | Design decisions trace cleanly to DD-1..DD-4 and the C1-C6 mapping; the gap is in what was *not* asked, not in traceability of what was |

---

*Devil's Advocate execution by adv-executor (blind, Group 3 of 6: Challenge). Strategy: S-002 per `.context/templates/adversarial/s-002-devils-advocate.md`. H-16 compliance confirmed against `adv-s003-steelman-optionc.md` (Group 2). Persisted per P-002.*
