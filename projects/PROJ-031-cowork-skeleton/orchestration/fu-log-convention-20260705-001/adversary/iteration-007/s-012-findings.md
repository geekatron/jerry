# FMEA Report: FEEDBACK-LOG + LLM-DECISION-LOG Convention (iteration-007, VERIFIED-CRITICALS round)

**Strategy:** S-012 FMEA (Failure Mode and Effects Analysis)
**Deliverable:** `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md` + 5 files in `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/` (`feedback-decision-logs-standards.md`, `FEEDBACK-LOG.template.md`, `LLM-DECISION-LOG.template.md`, `examples-appendix.md`, `hook-design-note.md`)
**Criticality:** C4 (gate 0.95)
**Date:** 2026-07-06
**Reviewer:** adv-executor (S-012 FMEA, blind protocol, iteration 007)
**H-16 Compliance:** S-003 Steelman ran first in every prior round of this tournament (iterations 001-006, confirmed from readable disposition history). Iteration-007's own S-003 output exists but was **not read** (blind protocol — this agent reads only its own output file and `restore-notes.md`). H-16 compliance is inferred from the established 7-round sequence pattern, not directly re-verified this round.
**Elements Analyzed:** 12 (package-wide, git-lifecycle-focused) | **Failure Modes Identified:** 4 (all newly surfaced this round; zero re-derivations of disclosed residuals) | **Total RPN:** 1196

## Navigation

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment and recommendation |
| [Scope Note](#scope-note) | Why this round targets git-lifecycle failure modes specifically |
| [Element Inventory](#element-inventory) | The 12 elements decomposed for this pass |
| [Findings Table](#findings-table) | All 4 findings with S/O/D/RPN |
| [Finding Details](#finding-details) | Full evidence, rationale, corrective action per Critical finding |
| [Recommendations](#recommendations) | Prioritized corrective actions |
| [Scoring Impact](#scoring-impact) | Mapping to the 6 S-014 dimensions |
| [Non-Findings](#non-findings) | Candidate gaps considered and rejected as already-disclosed |

## Summary

This package has been through six adversarial tournament rounds (RT/DA/PM/CC/CV/FM/IN across S-001/002/004/007/010/011/012/013) plus an owner RESTORE pass, and the corpus of disclosed residuals is exceptionally dense (see `restore-notes.md` and the design doc's Revision Changelog, v1-v9). Per the task's instruction, re-deriving any of those disclosed residuals is **not** a finding. This pass therefore targeted a category the prior six rounds gave comparatively little attention to: **the package's dependency on git as the durability/integrity substrate, examined across its actual multi-branch, multi-clone, multi-worktree operational lifecycle** — not just the single-session, single-clone case the existing disclosures cover. Three **Critical** and one **Major** failure mode were found, all newly surfaced (verified against all 6 staged files plus the design doc; none appear in the Revision Changelog, the RESTORE notes' Residuals Disclosed table, or any of the currently-readable prior-iteration disposition tables). All four are closeable by **disclosure or a one-line procedural note**, consistent with the package's own "simplify or disclose; never add machinery" doctrine — none requires new lint, file, field, or subsystem. **Recommendation: REVISE** — the three Critical findings should be closed by targeted disclosure (the same low-cost pattern that closed all but one of the iteration-006 Criticals) before this package is treated as ratification-ready on the "never lost" and "honest metadata" purposes.

## Scope Note

The four purposes given for this review are: feedback/decisions never lost; operator-burden-free capture; navigable growth; honest metadata. All four findings below trace directly to at least one of these purposes and are argued explicitly in each Finding Detail.

## Element Inventory

| ID | Element |
|----|---------|
| E1 | Design doc L0 — Executive Summary / purpose framing |
| E2 | Design doc L1.1 — FEEDBACK-LOG schema, redaction carve-out, id/alias scheme, single-writer discipline |
| E3 | Design doc L1.2 — LLM-DECISION-LOG schema, verbatim tradeoff, DEC/ADR boundary |
| E4 | Design doc L1.3 — Automation / hook design |
| E5 | Design doc L1.4 — Segment rotation, linked-list, parity check, tamper-evidence caveats |
| E6 | Design doc L2 — Governance, L5 lint, adoption/install plan, Backfill mechanics |
| E7 | Rule file `feedback-decision-logs-standards.md` — LOG-M-001..006, L5 Lint, Boundaries |
| E8 | `FEEDBACK-LOG.template.md` |
| E9 | `LLM-DECISION-LOG.template.md` |
| E10 | `examples-appendix.md` |
| E11 | `hook-design-note.md` |
| E12 | **Cross-artifact: the git-lifecycle substrate** (branches, worktrees, clone depth, history rewrite) that E2/E5/E7 explicitly rely on for durability and tamper-evidence, examined across the package's real multi-branch/multi-worktree operating context |

## Findings Table

| ID | Element | Failure Mode | S | O | D | RPN | Severity | Corrective Action | Affected Dimension |
|----|---------|-------------|---|---|---|-----|----------|-------------------|--------------------|
| FM-001-i7fmea | E2/E7 (LOG-M-002 redaction carve-out) | "Redacted in place" edits only the current working-tree text; the pre-redaction plaintext (incl. a real secret) remains permanently readable in git history, and the design's own anti-squash/anti-rewrite stance (kept for tamper-evidence) forecloses the one remediation that would actually remove it | 9 | 6 | 9 | 486 | Critical | Add a one-clause disclosure to LOG-M-002 + design L1.1: redaction removes the span from the *current* file text only, not from git history; true removal requires a separate history-rewrite, which conflicts with the tamper-evidence preference stated for sealed segments | Internal Consistency, Evidence Quality |
| FM-002-i7fmea | E2/E5/E7 (single-writer-per-log discipline, LOG-M-005 scope boundary) | The scope boundary names 3 undefended concurrent-writer categories (two terminal windows, a detached `background: true` task, a direct hand-edit) but omits a 4th, structurally different one: git-worktree/branch-isolated sessions, a capability this same framework advertises (`isolation: worktree`). Divergent worktrees each mint ids independently from what they see on disk; a later merge/rebase, if resolved naively, can **silently discard** an entire branch's captured entries with zero lint coverage (the surviving side stays contiguous — nothing looks wrong) | 8 | 5 | 8 | 320 | Critical | Add worktree/branch divergence as a 4th named category in the Scope-boundary bullet (design L1.1) + LOG-M-005, and add one documented conflict-resolution rule: never discard a conflicting hunk on these files; renumber the later-resolved side's ids past the surviving max and fix any `Superseded by`/cross-references it touches | Completeness, Internal Consistency |
| FM-003-i7fmea | E5/L1.4 (sealed-segment tamper-evidence backstop) | The "diff backstop has two preconditions" (linear history; commit granularity) omits a third: **clone depth**. A shallow clone (e.g. CI's common `fetch-depth: 1` default — the exact CI this design proposes wiring the L5 lint into) has no prior commits to diff against, so the tamper-evidence claim is silently false for that view of the repo even though full history exists on the remote | 7 | 6 | 7 | 294 | Critical | Name clone depth as a third precondition alongside the existing two (design L1.4 sealed-segments row; rule file L5-Lint intro); recommend (not mandate) `fetch-depth: 0` for whichever CI job runs the L5 lint | Internal Consistency, Methodological Rigor |
| FM-004-i7fmea | E1/E6 (Backfill chronology mechanics) | `datetime` is specified as date-only (`YYYY-MM-DD`, no time), but the design's own chronology-recovery rule for backfilled entries ("sort by Context `datetime` for chronology, not by canonical id") needs finer-than-daily granularity whenever two or more items are backfilled against the same historical date — the one field named authoritative for this purpose cannot fully order same-day items | 4 | 4 | 6 | 96 | Major | State the tie-breaker explicitly: same-`datetime` backfilled rows are ordered by promotion/insertion order (wording-only; no new field) | Traceability |

**Total RPN: 1196** (3 Critical + 1 Major). All four are net-new; none restates a disclosed residual from the Revision Changelog or `restore-notes.md`.

## Finding Details

### FM-001-i7fmea: Redaction is a working-tree edit; git history keeps the secret forever

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical (RPN 486) |
| **Element** | Design doc L1.1 (redaction carve-out); rule file LOG-M-002 |
| **Purpose blocked** | "honest metadata" (the integrity/safety claim is incomplete) and, indirectly, "operator-burden-free capture" (a safety net that doesn't hold shifts the real burden back onto the operator to pre-vet every utterance) |

**Evidence:**
- Design doc L1.1, line 65: *"Because the redaction is the one sanctioned, lower-scrutiny edit to a sealed entry, it must carry the same 'presence, not veracity' discipline every other trust-sensitive check does... Redaction is irreversible in the repo, and that transcript carries the same unenforced-retention / cross-machine-portability dependency already disclosed for Q1 — so a false-positive redaction of non-secret text can become permanently unrecoverable (IN-002)."*
- Rule file `feedback-decision-logs-standards.md`, line 24 (LOG-M-002): *"Redaction is irreversible in the repo; its only recovery path is the out-of-repo transcript, which carries the same unenforced-retention dependency disclosed for Q1 (IN-002)."*
- Design doc L1.4, line 197: the package's stated integrity preference is **against** rewriting history — *"a squash-merge or history rewrite can collapse the per-edit tamper-evidence trail, so treat log files as squash-exempt where the workflow allows."*

**Analysis:** Both cited passages disclose the risk of over-redaction (losing text that *wasn't* actually a secret, because the redacted span cannot be restored from the file itself). Neither passage — nor anywhere else in the six files — discloses the inverse and more severe risk: when a **real** secret is captured verbatim (the LOG-M-002 default, "verbatim wins," before anyone notices it needs redacting) and is later "redacted in place" as the one sanctioned edit to an already-sealed, already-committed entry, that edit only changes the *current* text of the file. The commit that introduced the plaintext secret is untouched and remains fully readable via ordinary `git log -p` / `git show` on that path, indefinitely. This is not a hypothetical: the RESTORE notes for this very package document exactly this capture-then-clean-up sequence happening twice (`restore-notes.md` Step 3: *"Employer-internal token set... 2 hits found... Both genericized"*; design doc line 30 cites the project's own prior `FU.4` sanitization pass as the model this carve-out is "modeled on"). The package's own stated preference to avoid squash-merge/history-rewrite (kept specifically *for* tamper-evidence, L1.4 line 197) is in direct, unacknowledged tension with the one operation that would actually remove a leaked secret from history. For a convention whose target repos include at least one public one (this project's own standing hygiene directive: never push employer-internal or codename references to the public framework repo; strip/obfuscate before any push — `[INFERENCE]`, drawn from this session's own operating context, not from the deliverable text), an unremoved plaintext secret sitting in reachable git history is a real, not cosmetic, failure against "honest metadata" / safe capture — the claim that a "redacted" entry is safe is not accurate once a real secret was captured even once before the redaction ran.

**Recommendation:** One-clause disclosure at LOG-M-002 (and design L1.1): state plainly that in-place redaction edits only the current file text, not git history, and that removing a leaked secret from history requires a separate, out-of-band history rewrite that is in tension with this package's own squash/rewrite-avoidance stance for sealed segments. No new lint, field, or subsystem required — this closes by wording, matching every prior Critical closure in this tournament.

---

### FM-002-i7fmea: The single-writer scope boundary enumerates 3 undefended categories; git worktrees are a 4th, and its failure mode is silent loss, not clobber

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical (RPN 320) |
| **Element** | Design doc L1.1 (Scope boundary bullet); rule file LOG-M-005 |
| **Purpose blocked** | "feedback/decisions never lost" (directly) |

**Evidence:**
- Design doc L1.1, line 79: *"Scope boundary (what this does NOT cover). The single-writer discipline holds only within one live orchestrating session. Two independent top-level sessions on the same project (e.g. two terminal windows), a detached `background: true` task that outlives its orchestrator's turn, or a direct human hand-edit of the file all bypass the orchestrator append path and remain a full last-write-wins race — undefended by this convention and invisible to lint 2."*
- Design doc L1.1, line 78: the concurrent-writer mitigation is scoped to "within one live session" and relies on the P-003 orchestrator-worker handoff to serialize appends.

**Analysis:** All three named undefended categories share one property: they are simultaneous, live processes racing on the **same file on disk**, so the failure signature is last-write-wins clobber. Git worktrees are structurally different and are not named anywhere in the six files (confirmed by search — "worktree" does not appear in the design doc or any staged file). A worktree is a *separate* working-directory checkout of the same repository, each with its own independently mutable copy of a project-scoped log path; two worktrees on two branches do not race live on one inode, they diverge asynchronously via git history and are reconciled later by a merge or rebase. This is not a remote possibility for this exact package: this review is itself running from a worktree checkout (`.../jerry-wt/feat/proj-030-skeleton-branch`), and the framework's own agent-definition standard exposes `isolation: worktree` as an official capability for background task isolation — i.e., the mechanism the design already discusses (background agents returning candidates for the orchestrator to append, line 78) can itself be dispatched into a separate worktree, at which point the "orchestrator appends" mitigation no longer applies because the orchestrator and the background task are no longer sharing one working copy of the file at all. When two such branches both append entries and are later merged, the log file is essentially guaranteed to conflict (both sides append at the tail). If a human or agent resolves that conflict by naively taking one side ("ours"/"theirs" — a common fast-path in an active session), the discarded side's entries vanish with **no gap left behind** to trip lint 2's contiguity check, and no other mechanism in the package would ever notice — this is a strictly worse failure signature than the already-disclosed live-clobber case, because it produces a *clean-looking*, fully contiguous file that is nonetheless missing real feedback, directly against the "never lost" purpose.

**Recommendation:** Extend the existing Scope-boundary bullet (design L1.1) and LOG-M-005 with a fourth named category (git-worktree/branch divergence), and add one procedural rule for resolving a conflict on these files: never discard a conflicting hunk — merge by preserving both sides' entries in id order, and if canonical ids collide, renumber the later-merged side to continue after the surviving maximum id and repair any `Superseded by:`/`Related:` references it carries. This is a documentation-only fix in the same register as the existing rotation procedure (design L1.4 Steps 1-4); no new lint is required, though a future one-line CI check for leftover conflict markers in a committed log file could be named as optional future work (matching the package's existing "MAY be a future monitor" pattern for the secret-regex-scan idea).

---

### FM-003-i7fmea: The tamper-evidence backstop names two preconditions; clone depth is an unstated third

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical (RPN 294) |
| **Element** | Design doc L1.4 (sealed-segments row); rule file L5-Lint section intro |
| **Purpose blocked** | "honest metadata" (the sole disclosed integrity mechanism silently does not hold in a common, unremarked configuration) |

**Evidence:**
- Design doc L1.1, line 63: *"Integrity is by convention, git-backstopped... Git history is the backstop: a tampering edit surfaces as a reviewable diff on these files, not silent corruption."*
- Design doc L1.4 (sealed-segments table row), line 197: *"Caveat — the diff backstop has two preconditions: (a) reasonably linear history — a squash-merge or history rewrite can collapse the per-edit tamper-evidence trail... and (b) commit granularity — an edit made and committed together with the original entry inside one milestone-cadence commit window produces no separate diff to review..."*
- Design doc adoption plan, line 254: the L5 lint is proposed to be *"implement[ed] and wire[d]... into the existing CI/lint pipeline"* and made *"wired AND required (branch-protected)."*

**Analysis:** The design doc itself explicitly enumerates the backstop's preconditions as exactly two ("(a)... and (b)..."), which is a precise, falsifiable claim I can check directly: there is a third precondition the doc does not name — the local clone must actually contain the prior history to diff against. A shallow clone (`git clone --depth 1`, or GitHub Actions' `actions/checkout` default of `fetch-depth: 1`) has no earlier commits at all for that job's working copy; a tampered or reworded "sealed" entry in a shallow checkout is indistinguishable from an original one, because there is nothing locally to diff it against. This is not an edge case reachable only by unusual operator behavior (unlike squash-merge, which requires someone to actively choose it) — it is the *default* checkout behavior of the exact CI system this package proposes wiring its own L5 lint into (line 254). The result: the "git-backstopped" integrity claim (line 63) is true for a full clone and silently false for the CI job meant to enforce this very convention, and nothing discloses that distinction.

**Recommendation:** Add clone depth as a named third precondition next to the existing two (design L1.4 sealed-segments row; propagate the phrase into the rule file's L5-Lint intro, matching how the other two preconditions already appear there). Recommend, as a non-mandatory implementation note on the install step, that the CI job running the L5 lint use full history (`fetch-depth: 0` or `git fetch --unshallow`) — a one-line CI config change, not new application machinery.

---

## Recommendations

| Priority | ID | Corrective Action | Est. Post-Correction RPN |
|----------|----|--------------------|--------------------------|
| 1 | FM-001-i7fmea | One-clause disclosure: redaction is working-tree-only; history rewrite is the actual remedy and is in tension with the squash-avoidance stance | ~40 (residual: operators must still separately decide whether to rewrite history for a real leak — an accepted, disclosed trade, not a new mechanism) |
| 2 | FM-002-i7fmea | Name git-worktree/branch divergence as a 4th scope-boundary category; add a one-rule merge-conflict resolution procedure (never discard a hunk; renumber on id collision) | ~48 (residual: still no automated enforcement of the resolution rule — a documented discipline, consistent with how LOG-M-005 already treats the other 3 categories) |
| 3 | FM-003-i7fmea | Name clone depth as a third backstop precondition; recommend `fetch-depth: 0` for the CI job running the L5 lint | ~42 (residual: a full local clone elsewhere still holds the true history; the gap is a documentation/CI-config gap, not a data-loss gap) |
| 4 | FM-004-i7fmea | State the same-`datetime` tie-breaker (promotion/insertion order) in the Backfill mechanics text | ~24 |

All four corrective actions are wording/disclosure/one-line-config only — zero new lint, file, field, or subsystem — consistent with this package's own established remediation pattern across iterations 001-006.

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | FM-002: the single-writer scope boundary's enumeration of undefended categories is incomplete (3 of 4 real categories named) |
| Internal Consistency | 0.20 | Negative | FM-001: squash/rewrite-avoidance (for tamper-evidence) is in unacknowledged tension with redaction-as-remedy; FM-003: the doc's own "two preconditions" claim is falsified by a third, unstated one |
| Methodological Rigor | 0.20 | Negative | The exhaustive disclosure methodology visible everywhere else in this package (six rounds of propagation sweeps) was not applied with equal rigor to the git-lifecycle dimensions (branch/worktree/clone-depth) of the same git-dependent durability and integrity model |
| Evidence Quality | 0.15 | Neutral | Findings are grounded in precise, quoted textual citations (esp. FM-003's literal "two preconditions" enumeration) and one piece of labeled environmental corroboration (`[INFERENCE]`: this review's own worktree path) for occurrence estimates |
| Actionability | 0.15 | Positive | All four corrective actions are lean wording/disclosure fixes matching the package's own anti-bloat doctrine; none requires new machinery |
| Traceability | 0.10 | Positive | Every finding cites a specific file, line, and existing rule id (LOG-M-002, LOG-M-005, L1.4 sealed-segments row) rather than introducing new taxonomy |

## Non-Findings

Candidate gaps considered during this pass and **rejected** as already covered by disclosed residuals (per the task instruction, re-deriving these is not a finding):

- Concurrent same-machine writers / last-write-wins race — disclosed (design L1.1 Scope boundary; LOG-M-005).
- Segment-rotation interruption / crash recovery — disclosed (design L1.4 rotation procedure Steps 1-4; IN-003/FM-004 per Revision Changelog v6-v7).
- Cross-project discovery burden (no unified index) — disclosed (design L1.1 Multi-scope discovery caveat).
- Backfill Queue source rot (memory/transcript may rotate) — disclosed (design doc Q4 mechanics).
- Rule-file token-budget overage — disclosed and standing [USER-DECISION] across every round since v3.
- Silent non-capture / no proactive detector — disclosed and elevated to explicit Q5 (v6/RT-005).
- L5 lint bypass via `--no-verify` — disclosed (rule file L5-Lint intro; design L2).

---

## Execution Statistics
- **Total Findings:** 4
- **Critical:** 3
- **Major:** 1
- **Minor:** 0
- **Protocol Steps Completed:** 5 of 5
