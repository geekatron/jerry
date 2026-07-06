# LLM-DECISION-LOG — PROJ-031-cowork-skeleton

> Captures decisions made in user↔LLM interaction: verbatim exchanges, summaries, model, session, datetime, context. Per FU.2 (2026-07-05).
> **Status: ACTIVE bootstrap.** Entries DEC-LLM-001–003 are real and preserved. The schema now tracks the **revised** Jerry convention (segment rotation, logger-assigned ids + verbatim aliases — see `design/feedback-decision-log-convention-design.md`), **pending final user ratification**. Scoping rule (per FU.2): project-scoped file when a Jerry Project is active; repo-root file otherwise.
> **Distinct from worktracker `DEC-NNN` entities:** those are work-item-scoped decision documents; this log is the interaction-level record of what was decided *between user and LLM* and under what context. Entries cross-link to DEC/ADR artifacts where they exist.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Entry Schema (bootstrap)](#entry-schema-bootstrap) | Fields until the framework convention lands |
| [DEC-LLM-001 scheme-b-ratified](#dec-llm-001-scheme-b-ratified) | ADR identity scheme locked |
| [DEC-LLM-002 subtraction-pass-authorized](#dec-llm-002-subtraction-pass-authorized) | Remediation approach + 0.95 gate |
| [DEC-LLM-003 fu-decision-log-conventions](#dec-llm-003-fu-decision-log-conventions) | New framework conventions commissioned |
| [Backfill Queue](#backfill-queue) | Pre-log decisions to retro-capture from transcripts |

## Entry Schema (bootstrap)

**Decision** (one sentence) · **User verbatim** (full — user text is short and authoritative) · **Assistant verbatim** (the decision-relevant excerpt, with transcript pointer to the full turn — full multi-page turns would bloat the log; final policy is an open design question) · **Summary/consequences** · **Context** (datetime, session id, model, agent/workflow ids, artifacts).

Shared context for DEC-LLM-001..003: **datetime** 2026-07-05 · **session** `fd8559c2-abdd-4da7-b29a-ef4895fa5248` · **model** `claude-fable-5` (user messages authored by human; assistant turns before 2026-07-02 were `claude-opus-4-8`) · transcript: `[transcripts]/fd8559c2-abdd-4da7-b29a-ef4895fa5248.jsonl`.

**Rotate at the cap:** seal this file and start a new segment at **~50 entries or ~800 lines** (whichever first), continuing ids monotonically (segment rotation, per the convention design). The cap is stated here so it is legible from this log alone.

---

## DEC-LLM-001 scheme-b-ratified

**Decision:** Jerry's canonical ADR identity is **Scheme B — subject-encoded** (`ADR-{domain-slug}-NNN`, origin in frontmatter, promotion = pure `git mv`); the promotion-is-the-point assumption is **ratified by the user** (P-020).

**User verbatim:**
> I ratify the promotion-is-the-point apporach and lock Scheme B.

**Assistant verbatim (decision-relevant excerpt from the preceding turn):**
> "The trade study proved the winner is entirely a referendum on one belief: baseline weights → two-namespace C wins; promotion-is-normal weights → B wins […] The evidence for 'promotion is normal': it's literally Jerry's thesis ('accrues knowledge, wisdom, experience'), and 100% of existing framework ADRs got to `docs/design/` via promotion. I recommend ratifying promotion-is-the-point → B. But it's your framework-trajectory call."
(Full turn: transcript above, assistant turn reporting workflow `wf_dcb52638-593` results.)

**Summary/consequences:** (a) Subject-encoded IDs canonical for all new ADRs; (b) project-scoped `ADR-PROJ031-NNN` demoted to permitted-but-discouraged dialect, **grandfathered in place** — the 2026-07-02 rename of PROJ-031's three ADRs stands, no re-rename; (c) bare `ADR-NNN` deprecated for new ADRs; (d) `ADR-PROJ031-004` self-promotes to a domain-slug id per its own Meta-Note when installed; (e) MEDIUM-tier enforcement only (HARD ceiling 25/25).

**Context:** Decision produced by workflow `wf_dcb52638-593` (nse-explorer trade study; 3 blind advocates; ps-architect ADR; 5 blind 10-strategy tournaments — decision layer survived all rounds: "none of the findings overturn the core naming-convention decision"). Evidence: `decisions/ADR-PROJ031-004-adr-identifier-convention.md` §Decision D-1..D-5; `orchestration/adr-convention-20260702-001/explore/trade-study.md` (winner-flip sensitivity, crossover C2≳22). Related: FEEDBACK-LOG FU.0.

---

## DEC-LLM-002 subtraction-pass-authorized

**Decision:** Remediate the ADR-convention package by **subtraction** (not further addition) and re-verify to a **≥0.95** gate.

**User verbatim:**
> I authorize the subtraction pass. I want us to get to >=0.95 and would like to understand what we have to get to this quality score.

**Assistant verbatim (decision-relevant excerpt from the preceding turn):**
> "The fix is subtraction, not a sixth additive round: cut the rule draft to ~2.5k tokens (sized like the other `*-standards.md`), shrink the lint to a minimal fail-closed core (≤5 rules), and close most of the 10 Criticals by *deleting* the over-claimed machinery. Then one focused re-verify against the gate."

**Summary/consequences:** ps-architect subtraction pass (token budget ~2.5k for the rule draft; lint ≤5 fail-closed rules; delete waiver ledger / two-tier ratification / CODEOWNERS-dependent claims; explicit disposition for each of iteration-005's 10 Criticals) followed by blind tournament iterations 006–008 (RT-M-010 C4 ceiling 10 total; 5 used). Root-cause being corrected: additive-remediation spiral — each round added enforcement machinery that became the next round's attack surface (iteration-005 composite 0.66, IC 0.52; PM-001 rule draft ~30k tokens vs ~12.5k L1 budget for all 17 rules files combined).

**Context:** Workflow launched 2026-07-05 (id recorded on dispatch; see FEEDBACK-LOG FU.1 disposition). Prior evidence: `orchestration/adr-convention-20260702-001/adversary/iteration-005/s-014-quality-score.md`.

---

## DEC-LLM-003 fu-decision-log-conventions

**Decision:** Commission two Jerry Framework conventions — a **Feedback/Follow-Up log** and an **LLM Decision Log** — designed via jerry:* background agents, modeled on and improving the [internal-kb] rules; installation gated on user design sign-off + adversary review.

**User verbatim:** See FEEDBACK-LOG.md → FU.2 (full text; kept single-sourced there).

**Assistant verbatim:** This entry and the launched research+design workflow constitute the response (same turn; transcript pointer above).

**Summary/consequences:** (a) Bootstrap logs created immediately (this file + FEEDBACK-LOG.md) so FU.0–FU.2 survive regardless of design timeline; (b) ps-researcher extracts [internal-kb] FU-log rules verbatim + inventories Jerry's capture mechanisms (hooks/session ids, worktracker DEC entity, transcripts, MEMORY) → ps-architect designs the convention + stages templates; (c) framework install is AE-002 auto-C3 minimum → adversary gate before `.context/rules/` changes; (d) future ADR: `ADR-feedback-decision-logs-001` (first born-Scheme-B ADR).

**Context:** Related: FEEDBACK-LOG FU.2 (verbatim + disposition). [internal-kb] sources: `[internal-kb]/.context/current/rules.md` + `*follow-up*.md` examples.

---

## Backfill Queue

Decisions made before this log existed (retro-capture from transcripts pending user authorization):

| Approx date | Added | Decision | Where recorded today |
|---|---|---|---|
| 2026-06-29 | 2026-07-05 | Accept design-phase ceiling (~0.86), proceed to Phase 3 (option a) | RESUME-CHECKPOINT.md |
| 2026-06-30 | 2026-07-05 | Repo name `geekatron/jerry-claude-plugin` (vendor-family pattern; YAGNI rejected) | `decisions/repo-naming-options.md` §Decision |
| 2026-07-02 | 2026-07-05 | Strip-set correction + c-007 gate (from live-test failures) | ADR-PROJ031-001 amendment; REQ-056 |
| 2026-07-02 | 2026-07-05 | Interim rename bare ADR-001..003 → ADR-PROJ031-00N | RESUME-CHECKPOINT.md; superseded in part by DEC-LLM-001 |
