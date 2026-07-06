# Pre-Mortem Report: Feedback/Decision Log Convention (FU-Log + LLM-Decision-Log Package)

**Strategy:** S-004 Pre-Mortem Analysis
**Deliverable:** `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md` + `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/{feedback-decision-logs-standards.md, FEEDBACK-LOG.template.md, LLM-DECISION-LOG.template.md, examples-appendix.md, hook-design-note.md}`
**Criticality:** C4 (engagement gate 0.95, user-set)
**Date:** 2026-07-06
**Reviewer:** adv-executor (S-004, iteration 2)
**H-16 Compliance:** S-003 Steelman applied in iteration 1 of this same tournament — confirmed via the deliverable's own self-reported changelog (`feedback-decision-log-convention-design.md` Revision Changelog v3 row, which cites `SM-001` as an addressed iteration-1 finding). `[INFERENCE — indirect confirmation]`: the S-003 output artifact itself was not read (blind protocol restricts this executor to its own output file under `adversary/iteration-002/`); confirmation rests on the deliverable's self-report.
**Failure Scenario:** It is 2027-07 (12 months out). The FEEDBACK-LOG/LLM-DECISION-LOG convention has quietly failed: the two bootstrap logs are still sitting under `projects/PROJ-031-cowork-skeleton/` in "ACTIVE bootstrap" status, never installed to `.context/rules/`; several real feedback items from intervening sessions are simply absent from the log with no trace; the one segment rotation that did occur split an entry across two files; and a standing directive the user gave twice is nowhere to be found because it landed in a different project's log the second time.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment and recommendation |
| [Findings Table](#findings-table) | All PM findings at a glance |
| [Finding Details](#finding-details) | Full detail for Critical/Major findings |
| [Recommendations](#recommendations) | P0/P1/P2 mitigation plan |
| [Scoring Impact](#scoring-impact) | Dimension-level impact mapping |

---

## Summary

Nine failure causes identified across all 5 Pre-Mortem category lenses (Technical, Process, Assumption, External, Resource). Two are **Critical** (P0): a stated safety net (the id-integrity lint) does not actually cover the most common concurrent-write failure mode (silent, traceless entry loss — exactly the "don't lose feedback" outcome the convention exists to prevent), and the entire enforcement chain lives in `design/staging-feedback-logs/` pending ratification with no deadline or escalation trigger for indefinite non-installation — the single root cause behind most of the 12-month failure modes the prompt names (abandoned logs, drifted ids, rotation never happening, missing entries). All fixes identified here are **textual/disclosure-only** (one sentence to a few lines each); none require new engineering machinery, consistent with the package's declared MEDIUM-tier anti-bloat posture. **Recommendation: REVISE (targeted, disclosure-only).**

---

## Findings Table

| ID | Failure Cause | Category | Likelihood | Severity | Priority | Affected Dimension |
|----|---------------|----------|------------|----------|----------|--------------------|
| PM-001-20260706 | Id-integrity lint does not catch the silent-overwrite (last-write-wins) concurrent-write failure mode | Technical | Medium | Critical | P0 | Internal Consistency |
| PM-002-20260706 | Convention lives only in `design/staging-feedback-logs/`, pending ratification, with no deadline/escalation for indefinite non-install | Process | High | Critical | P0 | Completeness |
| PM-003-20260706 | MEDIUM-tier rule has no skill trigger-map entry and (post-install) no L2 reinjection — more context-rot-vulnerable than the framework's own Tier B HARD rules | Technical | High | Major | P1 | Internal Consistency |
| PM-004-20260706 | Manual segment-rotation procedure verified only by the same actor that performed it | Process | High | Major | P1 | Methodological Rigor |
| PM-005-20260706 | No documented boundary between project-scoped FEEDBACK-LOG entries and cross-project MEMORY.md for standing/global directives | Assumption | High | Major | P1 | Completeness |
| PM-006-20260706 | "Segment Index... rebuildable by `ls`" overclaims recovery simplicity | Technical | Low-Medium | Minor | P2 | Internal Consistency |
| PM-007-20260706 | No grandfathering clause if a PROPOSED-DEFAULT (Q1-Q4) is rejected after entries already captured under it | Process | Medium | Minor | P2 | Completeness |
| PM-008-20260706 | Git-history "immutability backstop" for sealed segments assumes linear history; squash-merge could collapse the tamper-evidence trail | External | Low | Minor | P2 | Evidence Quality |
| PM-009-20260706 | No named owner for the ≤3 L5 lint implementation task at install time ("owner: this install step") | Resource | Medium | Minor | P2 | Actionability |

**Finding ID Format:** `PM-{NNN}-20260706` (execution_id = iteration date, this being iteration 2 of the S-004 strategy for this tournament).

---

## Finding Details

### PM-001: Id-integrity lint does not cover the silent-overwrite race [CRITICAL]

**Failure Cause:** The design's disclosed residual risk for concurrent writers states the id scheme is "collision-resistant, not collision-proof... it is backstopped by the id-integrity lint (L5 #2), which *detects* a duplicate/gap rather than *preventing* the race" (`feedback-decision-log-convention-design.md:70`). The lint itself is specified as checking only "unique, strictly increasing, and contiguous" ids (`feedback-decision-log-convention-design.md:201`, `staging-feedback-logs/feedback-decision-logs-standards.md:63`). A standard read-modify-append race — two writers (e.g. parallel/background agents, which FU.2's own verbatim request explicitly asked to leverage: `FEEDBACK-LOG.md:63`) reading the same stale file state and one write clobbering the other — produces **neither** a duplicate id **nor** a sequence gap in the final persisted file: the losing writer's entry is simply never on disk, and the winning writer's ids remain contiguous. This is the single most common naive-concurrency failure mode (last-write-wins), and it is not the "duplicate/gap" class the lint is built to catch.
**Category:** Technical
**Likelihood:** Medium — Jerry's own workflow model (background agents, `/orchestration`) makes concurrent appenders to the same project-scoped log a realistic scenario, not a contrived edge case.
**Severity:** Critical — the deliverable's own headline goal ("so that we don't loose feedback or follow up items," `FEEDBACK-LOG.md:59`, user verbatim) can be silently violated in a way the stated safeguard does not detect at all, which is a stronger failure than "detected but not prevented" — it is **undetected and unprevented**.
**Evidence:** `feedback-decision-log-convention-design.md:70-71` (residual-risk disclosure); `feedback-decision-log-convention-design.md:201` and `staging-feedback-logs/feedback-decision-logs-standards.md:63` (lint scope: uniqueness + monotonicity + contiguity only).
**Dimension:** Internal Consistency — the claim "backstopped by the id-integrity lint" implies real protective coverage for the concurrent-write case, but the lint's defined scope does not actually cover the silent-overwrite sub-case, so the claim and the mechanism do not match.
**Mitigation:** Reword the residual-risk disclosure to name the silent-overwrite/last-write-wins sub-case explicitly and state plainly that the lint does **not** catch it (only true duplicate/gap patterns are caught); reframe "single-writer-per-log append discipline" (LOG-M-005) from a background assumption into the actual load-bearing safeguard for this specific failure mode, since no lint can substitute for it. This is a wording change, not new machinery.
**Acceptance Criteria:** The design doc and standards file each state, in the residual-risk disclosure, that concurrent same-log writers can silently lose an entry with no lint signal, and that single-writer-per-log discipline (not the lint) is what prevents this.

### PM-002: Convention may never be installed — no deadline or escalation for indefinite non-ratification [CRITICAL]

**Failure Cause:** All enforcement (LOG-M-001..006, the ≤3 L5 lint checks, both templates) exists only under `design/staging-feedback-logs/`, gated on "Approve this design" (4 open PROPOSED-DEFAULTs, Q1-Q4) and then an AE-002/AE-003 adversary-gated install into `.context/rules/` (`feedback-decision-log-convention-design.md:208-217`, Adoption/migration plan steps 1-3). Per the repository's own auto-load model (only `.context/rules/` content is symlinked into `.claude/rules/` and loaded at session start — see `CLAUDE.md` Navigation table, "(A) = Auto-loaded"), **any future Claude Code session has zero automatic knowledge of this convention until install completes.** The Adoption plan has no deadline, no re-assessment trigger, and no escalation path for the case where ratification simply never happens or stalls indefinitely — the only re-assessment trigger in the whole document is scoped narrowly to the Q3 hook decision ("revisit the deferral at the first segment rotation or the first observed missed-capture incident," line 215), not to the overall install-never-happens risk. This is not a hypothetical: this very tournament is itself on adversary iteration 2 for this deliverable, and the sibling ADR-convention effort in this same project required a full multi-iteration subtraction pass before it shipped (`feedback-decision-log-convention-design.md:40`, citing the ADR-convention's own iteration-005 struggle) — indefinite or long-delayed ratification is an empirically grounded outcome in this project, not a contrived scenario.
**Category:** Process / Assumption
**Likelihood:** High — given the project's own precedent and the fact that the design is already mid-tournament at iteration 2 with no fixed install date.
**Severity:** Critical — if install never happens, none of LOG-M-001..006 is ever discoverable by a fresh session; this is the direct mechanism behind every one of the 12-month failure modes named in the prompt (abandoned logs, drifted ids, rotation never happening, missing entries), since a session that never loads the rule cannot follow it.
**Evidence:** `feedback-decision-log-convention-design.md:208-217` (Adoption/migration plan, no deadline language beyond narrow Q3 trigger); `.context/rules/mandatory-skill-usage.md` Trigger Map (no `FEEDBACK-LOG`/`LOG-M`/decision-log keywords present — confirmed absent); `CLAUDE.md` Navigation table (only `.context/rules/` content is auto-loaded).
**Dimension:** Completeness — the plan is missing the "what if ratification stalls" branch that every other design decision in this package receives (Q1-Q4 all have explicit fallback/default behavior; the install-timing risk itself does not).
**Mitigation:** Add one sentence to the Adoption/migration plan: an explicit re-assessment trigger for the overall install (not just Q3), e.g. "if this design is not ratified within N sessions/weeks, the bootstrap logs continue operating under the FU.2-only informal convention, and the owner flags the stall at the next status/commit-cadence checkpoint." Pure documentation; no new machinery.
**Acceptance Criteria:** Adoption/migration plan names a concrete re-assessment point (session count, calendar time, or event) for overall install stall, not only for the Q3 hook sub-decision.

---

### PM-003: No skill trigger / no L2 reinjection — self-undermining enforcement (summary; Major)

The convention's own governing principle is "what depends on the model remembering will eventually be forgotten" (`feedback-decision-log-convention-design.md:38`). Yet LOG-M-001..006 is MEDIUM-tier by construction (forced by the 25/25 HARD ceiling) and has no entry anywhere in `.context/rules/mandatory-skill-usage.md`'s trigger map — confirmed absent. Per `quality-enforcement.md`'s own Enforcement Architecture (L1 = "Vulnerable" to context rot, L2 = "Immune" via per-prompt reinjection) and Tier Vocabulary (MEDIUM rules do not receive L2-REINJECT markers; even Tier B HARD rules like H-16/H-17/H-18 get skill-based compensating controls), this convention would be enforced *purely* by L1 session-start rule awareness with zero compensating L2/L3 control — making it structurally *more* context-rot-vulnerable than any HARD rule in the framework, which is exactly the failure mode the convention exists to prevent. **Mitigation (disclosure-only, no new machinery required to close this Pre-Mortem finding):** add one sentence to the standards file noting this residual enforcement gap explicitly, so it is disclosed rather than silent.

### PM-004: Manual rotation, self-checked by the same actor (summary; Major)

Segment rotation (L1.4) is a rare (~once per 50 entries), multi-step manual procedure. Its only safeguard — "confirm the sealed segment's entry count matches the ACTIVE file's pre-seal count... a 5-second `grep -c`" (`feedback-decision-log-convention-design.md:177`) — is performed by the same agent that just executed the rotation, i.e. a same-actor self-check, not independent verification. Across many rotations and many different model sessions over 12 months, at least one botched rotation (split entry, wrong prev/next, off-by-one segment number) is plausible, and no lint check verifies rotation *content* parity — only final-sequence id contiguity, which a corrupted-but-contiguous rotation would still pass. **Mitigation:** specify the parity check as a printed, mechanical before/after `grep -c` comparison in the same turn (not an implicit mental check) — a wording precision fix, not new tooling.

### PM-005: No FEEDBACK-LOG ↔ MEMORY.md boundary for standing/global directives (summary; Major)

The design's own worked example (FU.3, commit-push-cadence) is captured as a project-scoped FEEDBACK-LOG entry **and separately** saved to persistent memory ("Saved to persistent memory as durable behavior," `FEEDBACK-LOG.md:76`; memory key `feedback-commit-push-cadence`, corroborated by the user's live `MEMORY.md`, which contains numerous parallel `feedback_*.md` entries). Neither the design doc nor the standards file documents when a standing/global directive should also be written to MEMORY.md, or prevents the two mechanisms from silently diverging. Since FEEDBACK-LOG is explicitly project-scoped-or-root (`feedback-decision-log-convention-design.md:87-89`), a standing directive captured only in one project's log is not automatically rediscoverable from a different, later project unless someone separately remembers the MEMORY.md write — which is already happening ad hoc, not by rule. **Mitigation:** one sentence in the standards file: "Standing/global directives that should apply across projects SHOULD also be persisted to MEMORY.md (or equivalent); FEEDBACK-LOG entries are project/root-scoped only."

---

## Recommendations

### P0 (Critical — MUST mitigate before acceptance)

- **PM-001-20260706:** Reword the concurrent-write residual-risk disclosure to name the silent-overwrite/last-write-wins failure mode explicitly and state the lint does not catch it; reframe single-writer-per-log discipline as the actual (not merely backstopped) safeguard. Acceptance: disclosure text updated in both the design doc and the standards file.
- **PM-002-20260706:** Add an explicit re-assessment/escalation trigger to the Adoption/migration plan for indefinite non-ratification (not only the narrower Q3 hook trigger). Acceptance: a concrete session-count, calendar, or event-based trigger is named in the plan.

### P1 (Important — SHOULD mitigate)

- **PM-003-20260706:** Disclose the "no skill trigger, no L2 reinjection" enforcement gap in the standards file.
- **PM-004-20260706:** Specify the rotation parity check as a printed, mechanical before/after comparison, not an implicit self-check.
- **PM-005-20260706:** Add a one-line rule distinguishing project-scoped FEEDBACK-LOG entries from cross-project MEMORY.md persistence for standing directives.

### P2 (Monitor — MAY mitigate; acknowledge risk)

- **PM-006-20260706:** Correct "rebuildable by `ls`" wording in both templates to reflect that canonical-id ranges require scanning segment content, not just listing filenames.
- **PM-007-20260706:** Add a grandfathering clause for entries captured under a PROPOSED-DEFAULT that is later rejected (mirrors the existing ADR-scheme grandfathering precedent in this same project).
- **PM-008-20260706:** Disclose that the git-history immutability backstop assumes linear (non-squashed) history for log files specifically.
- **PM-009-20260706:** Name a concrete owner (role or agent, not just "this install step") for the ≤3 L5 lint implementation task.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | PM-002, PM-005, PM-009: missing install-stall re-assessment trigger, missing MEMORY.md boundary rule, missing lint-implementation ownership |
| Internal Consistency | 0.20 | Negative | PM-001: claimed lint "backstop" does not match the lint's actual detection scope; PM-003: L0's own governing principle ("what depends on remembering will be forgotten") is undermined by the convention's own L1-only enforcement; PM-006: "rebuildable by ls" overstates recovery simplicity |
| Methodological Rigor | 0.20 | Negative | PM-004: same-actor self-check is a weak verification method for a rare, error-prone manual procedure |
| Evidence Quality | 0.15 | Neutral (minor negative) | PM-008: git-backstop claim does not account for squash-merge/rebase reality already evidenced in this project's own commit history; otherwise the package cites strong, specific evidence throughout |
| Actionability | 0.15 | Negative (cheaply resolvable) | PM-002, PM-004, PM-009: all fixes are one-line/one-clause textual additions, not new machinery — quickly actionable once flagged |
| Traceability | 0.10 | Neutral | Findings trace cleanly to specific design-doc line references and cross-check against `quality-enforcement.md`/`mandatory-skill-usage.md` SSOT; the package's own traceability discipline is otherwise sound |

**Result:** 2 Critical and 3 Major failure causes identified via prospective hindsight, all remediable through disclosure-only text edits (no new machinery), consistent with the package's declared MEDIUM-tier anti-bloat posture. Overall assessment: **REVISE (targeted)** — mitigate P0 findings before acceptance; P1 findings SHOULD be folded into the same revision pass since they are equally cheap; P2 findings MAY be deferred with the risk acknowledged.

---

*Strategy Execution: S-004 Pre-Mortem Analysis, iteration 2*
*Template: `.context/templates/adversarial/s-004-pre-mortem.md` v1.0.0*
*Constitutional: P-003 (no subagents), P-020 (draft-only, no framework-path writes), P-022 (evidence cited; inference labelled)*
