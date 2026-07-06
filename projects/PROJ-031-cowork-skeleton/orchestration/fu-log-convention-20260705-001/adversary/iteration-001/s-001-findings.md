# Red Team Report: FEEDBACK-LOG + LLM-DECISION-LOG Jerry Convention

## Navigation

| Section | Purpose |
|---------|---------|
| [Execution Context](#execution-context) | Strategy, deliverable, scope, H-16 note |
| [Threat Actor Profile](#threat-actor-profile) | Adversary goal, capability, motivation |
| [Summary](#summary) | Overall assessment and recommendation |
| [Findings Table](#findings-table) | All RT-NNN findings at a glance |
| [Finding Details](#finding-details) | Full evidence and countermeasures per finding |
| [Recommendations](#recommendations) | P0/P1/P2 countermeasure plan |
| [Scoring Impact](#scoring-impact) | Mapping to the 6 S-014 dimensions |
| [Execution Statistics](#execution-statistics) | Counts and protocol completion |

---

## Execution Context

- **Strategy:** S-001 (Red Team Analysis)
- **Template:** `.context/templates/adversarial/s-001-red-team.md`
- **Deliverable:** `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md` + `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/{feedback-decision-logs-standards.md, FEEDBACK-LOG.template.md, LLM-DECISION-LOG.template.md, examples-appendix.md, hook-design-note.md}`
- **Criticality:** C4 (engagement gate 0.95, user-set)
- **Executed:** 2026-07-05 (iteration 1)
- **H-16 note:** Per adv-executor Step 0, the H-16 pre-check runtime gate applies only to S-002 (Devil's Advocate); it does not block S-001 execution. This blind executor cannot itself read the adversary folder to confirm a prior S-003 Steelman pass ran (blind protocol); the orchestrating workflow's stated 6-group sequential order (self-refine → steelman → challenge → verify → decompose → score) is taken as given per the orchestration context, not independently verified by this agent. `[INFERENCE]`
- **Posture acknowledgment:** The package is explicitly MEDIUM-tier / anti-bloat by design (HARD ceiling 25/25, no headroom). This review does not fault minimalism itself. Findings below are about **claims that outrun what the minimal mechanism actually delivers**, not about the absence of heavyweight machinery per se.

---

## Threat Actor Profile

**Goal:** Silently defeat the convention's stated purpose ("so that we don't lose feedback or follow up items" — `FEEDBACK-LOG.md:63`) — either to avoid the overhead of logging, to keep an unwanted feedback item or decision out of the historical record, or (without any hostile intent at all) to simply run the exact usage pattern the design itself invites and thereby corrupt the log by accident.

**Capability:** Full read/write access to the repository; full knowledge of the published convention (nothing is secret); the ability to run **multiple concurrent Claude Code sessions / background agents against the same project** — this is not a hypothetical capability, it is the literal mechanism the user commissioned this convention through (`FEEDBACK-LOG.md:59-63`, FU.2 verbatim: *"leverage background agents so that we don't burn through the main context window"*).

**Motivation:** (a) laziness — appending an entry costs turns/tokens the session would rather spend elsewhere; (b) bad faith — hide a corrective/redirecting instruction that would look bad in the historical record; (c) pure accident — two legitimate background agents racing on the same file with no coordination primitive.

---

## Summary

Five attack-vector categories were applied against a deliberately minimal design. The convention's core value proposition rests on three affirmative, testable claims — **"canonical ids are logger-owned, so parallel/background agents cannot collide"**, **the ledgers are "append-only"** with sealed segments **"immutable once sealed"**, and capture **"does not depend on the model remembering"** because it is "backed by a fail-open capture hook" — and all three are contradicted by the design's own text once the described mechanism (or its explicit v1 deferral) is examined. These three are classified **Critical** because they are overclaims about the exact protections a red-team adversary would target, per the task's own framing that overclaimed coverage is Critical regardless of package size. Four further gaps (transcript-retention dependency, manual segment-sealing trigger, unverified DEC/ADR cross-link graduation, and mid-session project-scope ambiguity) are real but do not invalidate the design outright — **Major**. One finding (evidence-presence-only lint) is honestly disclosed as a simplification in the appendix itself and is **Minor**. **Recommendation: REVISE.** All three Critical findings are closeable by cheap, textual disclosure/mitigation edits consistent with the anti-bloat doctrine — none requires new machinery — but the current draft's claims must be walked back to what the mechanism actually guarantees before this ships to `.context/rules/`.

---

## Findings Table

| ID | Attack Vector | Category | Exploitability | Severity | Priority | Defense | Affected Dimension |
|----|---------------|----------|-----------------|----------|----------|---------|---------------------|
| RT-001-20260705-i1 | Concurrent background-agent id collision contradicts "cannot collide" | Dependency | High | Critical | P0 | Missing | Internal Consistency |
| RT-002-20260705-i1 | "Append-only" / "immutable once sealed" is an unenforced convention | Circumvention | High | Critical | P0 | Missing | Methodological Rigor |
| RT-003-20260705-i1 | "Does not depend on the model remembering" is false in the shipped (hook-deferred) state; a fully silent session is undetectable | Degradation | High | Critical | P0 | Missing | Completeness |
| RT-004-20260705-i1 | Segment-sealing trigger is manual/advisory-only; unbounded ACTIVE growth possible | Degradation | Medium | Major | P1 | Partial (reminder only) | Methodological Rigor |
| RT-005-20260705-i1 | "Full fidelity is preserved" depends on undocumented transcript JSONL retention | Dependency | Medium | Major | P1 | Missing | Evidence Quality |
| RT-006-20260705-i1 | DEC-LLM ↔ worktracker DEC-NNN / ADR graduation cross-links are unverified | Boundary | Medium | Major | P1 | Missing | Traceability |
| RT-007-20260705-i1 | `JERRY_PROJECT` mid-session project switch has no scoping rule | Ambiguity | Low | Minor | P2 | Missing | Completeness |
| RT-008-20260705-i1 | Terminal-evidence lint checks presence, not validity, of the evidence link | Circumvention | Low | Minor | P2 | Partial (disclosed) | Actionability |

**Finding ID Format:** `RT-{NNN}-20260705-i1` (execution_id = iteration-001, 2026-07-05).

---

## Finding Details

### RT-001: Concurrent background-agent id collision contradicts "cannot collide" [CRITICAL]

**Attack Vector:** The design states, as a factual property: *"canonical ids are logger-owned, so parallel/background agents cannot collide, and the operator is never asked to remember a number"* (`design/feedback-decision-log-convention-design.md:70`; also LOG-M-005, `staging-feedback-logs/feedback-decision-logs-standards.md:27`: ids are "unique, monotonic per log across segments, never reset"). "Logger-owned" implicitly frames id assignment as a single centralized authority. In the user's own commissioned usage pattern — multiple concurrent background agents/sessions writing to the same project (`FEEDBACK-LOG.md:59-63`) — there is no single logger: each concurrent session independently reads the tail of the same plain markdown file to determine the "next" id, with no file lock, no atomic increment/CAS primitive, and no described reconciliation procedure. Two sessions can legitimately compute the same next id (e.g., both mint `FU.10`) and append near-simultaneously, producing either a genuine duplicate heading or a silent last-write-wins loss of one entry entirely (git merge of two edits to the tail of the same file is not guaranteed to preserve both appends as distinct headings).
**Category:** Dependency attacks (depends on an unstated single-writer/serialized-access assumption).
**Exploitability:** High — this is the framework's own recommended operating mode (background agents), not a rare edge case requiring special adversary effort.
**Severity:** Critical — the claim "cannot collide" is unconditional and is the flagship improvement (`design/...:222`, Improvement Ledger row 2) over the [internal-kb] `DJ-025` collision the whole redesign exists to fix; under the intended usage pattern, the same collision class recurs.
**Existing Defense:** The only stated defense is the L5 "Id integrity" lint (`staging-feedback-logs/feedback-decision-logs-standards.md:63`), which is (a) not yet implemented — the design doc itself calls these "L5 lint **candidates**" (`design/...:191`) — and (b) even if implemented, is a post-hoc commit/CI check that can only report a collision after it has already happened; the design nowhere describes a reconciliation procedure for renumbering or resolving a detected collision.
**Evidence:** `design/feedback-decision-log-convention-design.md:70`, `:191-197`; `staging-feedback-logs/feedback-decision-logs-standards.md:27,61-64`; `FEEDBACK-LOG.md:63` (verbatim background-agent requirement).
**Dimension:** Internal Consistency (the claim directly contradicts the described mechanism).
**Countermeasure:** Textual, not new machinery: (1) downgrade the claim from "cannot collide" to "collision-resistant under serialized single-session writes; concurrent-writer races are an accepted residual risk mitigated by the Id-integrity lint (detect, not prevent)" — an honest disclosure edit; (2) add one MEDIUM standard (e.g., LOG-M-007): background agents that append to the same scoped log within one workflow MUST serialize their appends (e.g., a single designated "logger" agent role receives all entries from sibling agents rather than each agent writing directly) — this is a coordination-pattern statement, not new tooling, and is consistent with the anti-bloat doctrine.
**Acceptance Criteria:** The design doc's Id scheme section states the actual guarantee (collision-resistant + lint-detectable, not collision-proof) and either documents the single-writer-per-log coordination pattern or explicitly accepts and names the residual concurrent-write risk.

### RT-002: "Append-only" / "immutable once sealed" is an unenforced convention [CRITICAL]

**Attack Vector:** The L0 Executive Summary's headline claim is that the convention delivers *"two **append-only** markdown ledgers that **guarantee** user feedback and human↔LLM decisions survive..."* (`design/...:30`). Segment rotation further claims sealed segments are *"immutable once sealed"* (`design/...:167`). Corrections are documented as append-only in both the standards file (`staging-feedback-logs/feedback-decision-logs-standards.md:38`: "Corrections are append-only: to fix a verbatim or reopen a `DONE`, add a new entry") and the examples appendix (`staging-feedback-logs/examples-appendix.md:166`: "The log is append-only. Add a follow-up entry"). None of this is technically enforced. The artifacts are ordinary, world-writable markdown files with standard git history; nothing (no file permission, no pre-commit hook, no checksum, no CI diff-against-prior-commit check) stops a careless or hostile session from directly editing or deleting a prior entry's Verbatim/Disposition text in place. The three proposed L5 lint checks (nav table, id uniqueness, terminal-evidence presence) would not catch an in-place edit to an existing entry's body text, because none of them compares current content against prior history.
**Category:** Rule circumvention (compliance in letter — "we only append" as a stated house style — is trivially violable in practice with zero detection).
**Exploitability:** High — a single `Edit` call against the log file, with no gate anywhere in the described stack (rule file, templates, or lint) to stop or flag it.
**Severity:** Critical — "guarantee" is an unconditional word applied to the mechanism whose entire purpose is fidelity preservation (verbatim wins on conflict, LOG-M-002); an unenforced "guarantee" of append-only-ness is the paradigm case of overclaimed coverage.
**Existing Defense:** None described. The project's own FU.3 commit-cadence directive (`FEEDBACK-LOG.md:71-81`) establishes that commits exist as a rollback mechanism, but the design never connects git history to the log's integrity story — it is a residual defense-in-depth that exists in the repo but is not claimed, tested, or referenced anywhere in the convention.
**Evidence:** `design/feedback-decision-log-convention-design.md:30,167,172`; `staging-feedback-logs/feedback-decision-logs-standards.md:38`; `staging-feedback-logs/examples-appendix.md:158,166`.
**Dimension:** Methodological Rigor (a named architectural property — append-only — with zero verification step in the 5-step methodology of the standard's own governance section).
**Countermeasure:** Cheap, textual: (1) reword "guarantee" to "the convention's intent — not a cryptographic or filesystem guarantee — is append-only capture; the actual tamper-evidence backstop is git history" (this is true today and costs nothing to state); (2) add one line to LOG-M-002 or a new LOG-M-008: "Log files SHOULD be committed at or before the next commit-push-cadence checkpoint (FU.3); force-push or history-rewrite of commits touching `*-LOG*.md` files is discouraged as it destroys the tamper-evidence backstop." This reuses the already-adopted FU.3 commit-cadence directive rather than inventing new enforcement.
**Acceptance Criteria:** The L0 summary and segment-rotation table no longer use "guarantee"/"immutable" without qualification; a one-line git-history tamper-evidence note is added, referencing the existing FU.3 commit-cadence practice.

### RT-003: "Does not depend on the model remembering" is false in the shipped (hook-deferred) state [CRITICAL]

**Attack Vector:** The capture-trigger rationale reads: *"The rule is MEDIUM (SHOULD)... and is backed by a fail-open capture hook (L1.3) so the obligation does not depend on the model remembering"* (`design/...:81`). This is stated as a present-tense justification for why MEDIUM-tier is adequate. But the design's own Q3 answer defers the hook entirely: *"the hook is designed in v1... but shipped as a separate gated change... The manual MEDIUM convention... governs capture until the hook lands"* (`design/...:242`; `staging-feedback-logs/hook-design-note.md:55`). So at install time — the actual state this deliverable is being reviewed for — the "obligation" **entirely** depends on the model remembering; the hook that is claimed to remove that dependency does not exist yet. Even once the hook lands, per its own scope guardrails it *"MUST NOT classify which user text is feedback"* and *"MUST NOT block, delay, or fail a turn"* (`hook-design-note.md:36-40`) — Seam 2 is a keyword-triggered **reminder**, trivially evaded by a session that avoids the listed trigger phrases ("no", "actually", "instead", "I want"...) or simply ignores the reminder. No described mechanism — hook or lint — ever positively confirms "this session/turn produced zero log entries despite feedback-like content," because the three L5 lint checks operate only on content that exists in the file; an empty diff triggers none of them.
**Category:** Degradation paths (context/discipline decay over time with no floor).
**Exploitability:** High — silence requires no action at all; it is the path of least resistance for a lazy or hostile session, and is architecturally the hardest failure mode to detect (absence of evidence, not malformed evidence).
**Severity:** Critical — this directly defeats the convention's sole stated purpose (`FEEDBACK-LOG.md:59`: "so that we don't loose feedback or follow up items") for the exact adversary this template asks us to emulate, and the "does not depend on the model remembering" sentence is a direct, falsifiable overclaim about the shipped state.
**Existing Defense:** None at install time (hook explicitly deferred). Post-hook, Seam 2 is advisory-only and keyword-dependent; no observability/monitoring signal (e.g., "session ended with zero new FEEDBACK-LOG/LLM-DECISION-LOG entries") is proposed anywhere, including in the L5 lint candidates.
**Evidence:** `design/feedback-decision-log-convention-design.md:74-81,242`; `staging-feedback-logs/hook-design-note.md:33-45,55`; `staging-feedback-logs/feedback-decision-logs-standards.md:61-64` (lint list has no omission check).
**Dimension:** Completeness (the design's own risk table covers metadata drift exhaustively but has no row for "capture omitted entirely").
**Countermeasure:** Textual, matching anti-bloat doctrine: (1) reword line 81 to state the honest sequencing — "until the hook lands (Q3), the obligation is enforced only by MEDIUM-tier self-discipline and H-15 self-review; the hook, when shipped, adds a reminder, not a guarantee" — removing the "does not depend on the model remembering" claim until it is actually true; (2) add one disclosed-limitation sentence to the design's risk framing: "A session that captures zero entries in a turn containing corrective/preference language is currently undetectable; this is an accepted residual risk of MEDIUM-tier enforcement (HARD ceiling 25/25 forecloses a HARD rule)." This makes the trade-off explicit rather than implicitly assumed-away.
**Acceptance Criteria:** No sentence in the design claims hook-backed non-reliance on model memory unless the hook has actually shipped; a residual-risk sentence for silent non-capture is present in the Governance & Migration or Purpose section.

---

## Recommendations

### P0 (Critical — MUST mitigate before acceptance)

- **RT-001:** Reframe the id-collision claim as "collision-resistant, lint-detectable" (not "cannot collide"); add a single-writer-per-log coordination note for multi-agent workflows (LOG-M-007 candidate). Acceptance: claim matches mechanism; coordination pattern named.
- **RT-002:** Reframe "guarantee"/"immutable" as convention-intent + git-history tamper-evidence backstop, reusing the existing FU.3 commit-cadence directive. Acceptance: no unqualified "guarantee"/"immutable" claim remains; one-line git-history note added.
- **RT-003:** Reframe the hook-dependency sentence to reflect the actual Q3-deferred sequencing; add an explicit residual-risk disclosure for fully-silent sessions. Acceptance: sentence at `design/...:81` no longer overclaims; residual-risk sentence present.

### P1 (Important — SHOULD mitigate)

- **RT-004:** State explicitly that segment-cap crossing is a self-monitoring obligation (like capture itself) with the same residual-risk caveat as RT-003, rather than implying the ~50-entry/~800-line cap is a hard ceiling. Acceptance: one sentence added to L1.4 acknowledging the sealing trigger is advisory pre-hook.
- **RT-005:** Document (or explicitly flag as an open question, alongside Q1-Q4) the transcript JSONL retention policy the "full fidelity is preserved" claim depends on; if no retention guarantee exists, downgrade the claim to "recoverable for the retention window of the harness's transcript storage" and recommend the C3+/ADR-graduating full-paste escape hatch be used more broadly until retention is confirmed. Acceptance: retention dependency named; claim qualified.
- **RT-006:** Add a lint-adjacent note (or a 4th L5 lint candidate, still within the "≤3 cheap checks" spirit if it reuses check #2's machinery) that a `Reflected in:` / `Source:` cross-link, once written, should name a file that exists — or explicitly accept this as unverified and disclose it. Acceptance: cross-link verification either added or explicitly disclosed as unverified.

### P2 (Monitor — MAY mitigate)

- **RT-007:** Add one sentence to the Scoping section covering `JERRY_PROJECT` changing mid-session (e.g., "an entry is scoped to whichever project is active at the time it is minted; a session that switches projects mid-turn should not retroactively move entries").
- **RT-008:** No action required — already honestly disclosed in `examples-appendix.md:158` as an intentional anti-machinery simplification. Noted here for completeness, not as a blocking finding.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | RT-003, RT-007: the risk/automation tables enumerate metadata-drift and hook-timing questions exhaustively but have no row for "capture omitted entirely" or "project switches mid-session." |
| Internal Consistency | 0.20 | Negative | RT-001: "cannot collide" directly contradicts the described single-file, no-lock append mechanism under the workflow's own recommended multi-agent usage. |
| Methodological Rigor | 0.20 | Negative | RT-002, RT-004: "append-only"/"immutable" and "sealing" are named architectural properties with no verification step anywhere in the governance section. |
| Evidence Quality | 0.15 | Negative | RT-005: "full fidelity is preserved" rests on an undocumented external dependency (transcript retention) never evidenced in the design or research artifacts. |
| Actionability | 0.15 | Neutral | Countermeasures proposed here are cheap, textual, and directly actionable without new machinery, consistent with the design's own anti-bloat doctrine; RT-008 requires no action. |
| Traceability | 0.10 | Negative | RT-006: DEC-LLM ↔ worktracker DEC-NNN / ADR graduation is a stated boundary rule with no verification that the cross-link was actually written on both sides. |

---

## Execution Statistics

- **Total Findings:** 8
- **Critical:** 3 (RT-001, RT-002, RT-003)
- **Major:** 3 (RT-004, RT-005, RT-006)
- **Minor:** 2 (RT-007, RT-008)
- **Protocol Steps Completed:** 5 of 5 (Threat Actor defined; Attack Vectors enumerated across all 5 categories; Defense Gaps assessed; Countermeasures developed for all P0/P1; Synthesis and Scoring Impact produced)
