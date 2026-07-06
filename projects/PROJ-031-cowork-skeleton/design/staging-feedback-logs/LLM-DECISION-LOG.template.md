# LLM-DECISION-LOG — {SCOPE}

> Captures decisions made in user↔LLM interaction: verbatim exchanges, summaries, model, session, datetime, context. Per the Feedback & Decision Log Standards (`feedback-decision-logs-standards.md`).
> **Scope:** project-scoped (`projects/<PROJECT_ID>/`) when a Jerry Project is active; repo-root otherwise.
> **Distinct from worktracker `DEC-NNN` entities:** those are work-item-scoped, AST-validated decision documents with a state machine; this log is the low-ceremony **interaction-level** record. Entries cross-link to DEC/ADR artifacts; a hardened, work-item-attached decision **graduates** into a DECISION entity and/or ADR. The formal artifact wins on conflict.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Entry Schema](#entry-schema) | Fields |
| [DEC-LLM-001 example-entry](#dec-llm-001-example-entry) | Worked example (delete when real entries land) |
| [Backfill Queue](#backfill-queue) | Pre-log decisions pending retro-capture |

## Entry Schema

Each entry = `## DEC-LLM-NNN <slug>` (NNN monotonic within this file). Fields, fixed order:

- **Decision** — one sentence: what was decided.
- **User verbatim** — full (short, authoritative). If it already lives in FEEDBACK-LOG, single-source there and link (`See FEEDBACK-LOG FU.N`).
- **Assistant verbatim** — the decision-relevant excerpt + transcript pointer `{session_id}#{uuid}` (full turn recoverable from the immutable JSONL; excerpt keeps the log loadable).
- **Summary / consequences** — downstream effects.
- **Context** — `datetime · session · model · agents/workflow · artifacts`.

> **Assistant-verbatim policy is pending user ratification** (excerpt+pointer vs full paste). Until ratified, use excerpt+pointer.

---

## DEC-LLM-001 example-entry

**Decision:** {one sentence — the decision reached this turn.}

**User verbatim:**
> {paste the user's exact words, full — or `See FEEDBACK-LOG FU.N`}

**Assistant verbatim (decision-relevant excerpt):**
> {the recommendation / options / rationale / pushback that bears on the decision}

(Full turn: transcript `{session_id}#{uuid}`.)

**Summary / consequences:** {what follows from the decision; who/what it affects downstream.}

**Context:** datetime `{YYYY-MM-DD}` · session `{session_id}` · model `{model-per-turn}` · agents/workflow `{ids or —}` · artifacts `{paths}` · Reflected in `{DEC-NNN / ADR-… / commit / — }`

---

## Backfill Queue

Decisions made before this log existed (retro-capture from transcripts, pending user authorization):

| Approx date | Decision | Where recorded today |
|---|---|---|
| {YYYY-MM-DD} | {short description} | {artifact / checkpoint} |
