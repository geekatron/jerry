# LLM-DECISION-LOG — {SCOPE}

> The append log for decisions made in user↔LLM interaction, recorded *when captured* (a MEDIUM/SHOULD discipline, not a guarantee — see the standards): verbatim exchanges (secrets/PII redacted), summaries, model, session, datetime, context. Per the Feedback & Decision Log Standards (`feedback-decision-logs-standards.md`).
> **Scope:** project-scoped (`projects/<PROJECT_ID>/`) when a Jerry Project is active; repo-root otherwise.
> **Distinct from worktracker `DEC-NNN` entities:** those are work-item-scoped, AST-validated decision documents with a state machine; this log is the low-ceremony **interaction-level** record. Entries cross-link to DEC/ADR artifacts; a hardened, work-item-attached decision **graduates** into a DECISION entity and/or ADR. The formal artifact wins on conflict.
> **Segment 1 (ACTIVE)** · prev: — · next: — — the stable ACTIVE file; always read and append here.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Entry Schema](#entry-schema) | Fields, ids and aliases |
| [Segment Index](#segment-index) | Segment map for large logs |
| [DEC-LLM-001 example-entry](#dec-llm-001-example-entry-alias-) | Worked example (delete when real entries land) |
| [Backfill Queue](#backfill-queue) | Pre-log decisions pending retro-capture |

## Entry Schema

Each entry = `## DEC-LLM-NNN <slug> (alias: <your-label or —>)`. Like the FEEDBACK-LOG, **`NNN` is logger-assigned** (unique, monotonic across all segments, never resets); your label is kept verbatim as the alias — you never track a counter. Ids are collision-*resistant*, not collision-proof — only the orchestrating session appends; concurrent sessions or hand-edits can clobber (LOG-M-005). A background/worker candidate quotes the operator's (or the decision's) original words **unaltered**; the orchestrator appends that quoted text as the verbatim, never a paraphrase (RT-001). Fields, fixed order:

- **Decision** — one sentence: what was decided.
- **User verbatim** — full (short, authoritative). If it already lives in FEEDBACK-LOG, single-source there and link (`See FEEDBACK-LOG FU.N`).
- **Assistant verbatim** — the decision-relevant **excerpt** + transcript pointer `{session_id}#{uuid}` (the excerpt keeps the log loadable; the full turn is recoverable from the JSONL **while the transcript is retained and its pointer resolves on the reading machine**). *User text is kept full, assistant text is excerpted, because assistant turns run large — this keeps the log loadable; full fidelity depends on transcript retention (an unenforced dependency; design doc Q1), for which the C3+ full-paste option is the mitigation.*
- **Summary / consequences** — downstream effects.
- **Context** — `datetime · session · model · agents/workflow · artifacts · Reflected in`. A cross-log citation to the FEEDBACK-LOG renders as a labeled `Related: FU.N` (one consistent form, not ad-hoc prose); `Reflected in` carries the graduation cross-link (`DEC-NNN` / ADR). When the provenance hook is installed the assistant stamps this; **otherwise fill what you know** (until the Q3 hook ships). Append `scope: framework` only for a framework-level decision captured inside an active project (Q2, pending ratification); default `scope: project` need not be written. A repo-root entry about one project MAY add an optional `project: PROJ-NNN` tag (CV-003).
- **Reversal/supersession** — when a later decision reverses an earlier one, mark the old entry `Superseded by: DEC-LLM-NNN` (a status pointer — one of the two sanctioned edits to a sealed entry, symmetric with FEEDBACK-LOG's `Superseded by: FU.N`; the other is an in-place hygiene redaction; distinct from `Reflected in`, which is outward graduation only). RT-002.

> **Assistant-verbatim policy is a PROPOSED-DEFAULT** (excerpt+pointer vs full paste), pending user ratification. Until ratified, use excerpt+pointer; full paste is available for C3+/ADR-graduating decisions. Size math: design doc Q1.

## Segment Index

**Rotate at the cap:** seal this ACTIVE file and start a new segment at **~50 entries or ~800 lines** (whichever first) — ids continue monotonically; see the walkthrough in `examples-appendix.md` and LOG-M-006. (The cap is restated here so it is legible from the log alone, independent of whether the rule file is loaded — PM-002-iter8.)

Segment files are enumerable by `ls`; the id-ranges are read from each segment's first/last headings. One row per segment; the ACTIVE row is this file.

| Segment | File | Canonical ids |
|---------|------|---------------|
| 1 | LLM-DECISION-LOG.md (ACTIVE) | DEC-LLM-001 – … |

> **Forward-nav (travels with this file):** from a sealed segment N, open `LLM-DECISION-LOG.{N+1:03d}.md` if it exists, else the stable ACTIVE `LLM-DECISION-LOG.md`. A sealed segment's `next:` may name a not-yet-created successor — the ACTIVE file is always the tail. **Backward-nav:** follow `prev:`.

---

## DEC-LLM-001 example-entry (alias: —)

> Worked example (genericized from a real ratification decision). Delete when real entries land. Note the `(alias: —)` suffix — this decision was assistant-initiated, so the operator gave no label; every entry heading carries the suffix even when the alias is `—`.

**Decision:** Approach **B** (subject-encoded identity) is ratified as canonical; the load-bearing assumption is confirmed by the user (P-020).

**User verbatim:**
> See FEEDBACK-LOG FU.0    (single-sourced there; or paste the full user text)

**Assistant verbatim (decision-relevant excerpt):**
> "The trade study proved the winner turns entirely on one belief: baseline weights → the two-namespace option wins; promotion-is-normal weights → B wins. I recommend ratifying B — but it is your framework-trajectory call."

(Full turn: transcript `{session_id}#{uuid}`.)

**Summary / consequences:** B canonical for all new ADRs; the prior dialect is grandfathered in place; MEDIUM-tier enforcement only.

**Context:** datetime `{YYYY-MM-DD}` · session `{session_id}` · model `{model-per-turn}` · agents/workflow `{ids or —}` · artifacts `{paths}` · Reflected in `ADR-<domain-slug>-NNN`

---

## Backfill Queue

Decisions made before this log existed (retro-capture from transcripts, pending user authorization). Not a parking lot: rows carry an added-date and are reviewed at the same commit-cadence checkpoint as OPEN items — **capped at the next milestone or ~3 months, whichever first** — promoted to a full entry or explicitly declined — and sooner if a row's source (transcript/artifact) is observed to have rotated. On promotion, the item is tail-appended with the next canonical id (historical date in the body) and tagged `(backfilled)` until an independent reference (commit hash, transcript pointer) is cited in it.

| Approx date | Added | Decision | Where recorded today |
|---|---|---|---|
| {YYYY-MM-DD} | {YYYY-MM-DD} | {short description} | {artifact / checkpoint} |
