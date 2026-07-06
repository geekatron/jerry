# FEEDBACK-LOG — {SCOPE}

> Feedback / Follow-Up (FU) log — the append target for user feedback and follow-up items, captured **verbatim** *when logged* (capture is a MEDIUM/SHOULD discipline, not a guarantee — see the standards; secrets/PII redacted before capture), with disposition tracking. Per the Feedback & Decision Log Standards (`feedback-decision-logs-standards.md`).
> **Scope:** project-scoped (`projects/<PROJECT_ID>/`) when a Jerry Project is active; repo-root otherwise.
> **Segment 1 (ACTIVE)** · prev: — · next: — — this is the stable ACTIVE file; always read and append here.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Log Conventions](#log-conventions) | Entry schema, ids and aliases |
| [Segment Index](#segment-index) | Segment map for large logs |
| [FU.0 commit-push-cadence (alias: FU.0)](#fu0-commit-push-cadence-alias-fu0) | Worked example (delete when real entries land) |
| [Backfill Queue](#backfill-queue) | Pre-log feedback pending retro-capture |

## Log Conventions

Each entry = `## FU.N <slug> (alias: <your-label or —>)` with fields in fixed order: **Verbatim** (your exact words, typos preserved — verbatim means verbatim), **Summary** (assistant normalization), **Disposition** (`OPEN / IN-PROGRESS / DONE / WONTFIX` + evidence link on terminal states), **Context** (provenance line, includes `source` = `chat | inline-doc | transcript`). If you give no label, the alias is `—`.

**Ids & aliases — you never track a counter.** You label feedback however you like; you will typically restart at `FU.0` every turn and every document you review. That is expected. The **assistant assigns the canonical `FU.N`** (unique, monotonic across all segments, never resets) and records **your label verbatim as the `(alias: …)`**. Example: you type `FU.0, FU.1` this turn and `FU.0` next turn; the log records `FU.0 (alias: FU.0)`, `FU.1 (alias: FU.1)`, `FU.2 (alias: FU.0)`. More: `examples-appendix.md`.

> **Single-writer safety (the load-bearing caveat, LOG-M-005):** ids are collision-*resistant*, not collision-proof. Only **one writer** — the orchestrating session — should append; concurrent sessions/windows or direct hand-edits can silently clobber each other (an undefended last-write-wins race). Background agents return short *candidates* the orchestrator appends; they do not write here directly. A candidate carries your original words **unaltered** (a quoted sub-field), and the orchestrator uses that quoted text as the Verbatim — never a worker's paraphrase (RT-001).

- **Context** format: `datetime · session · model(s) · turn · agents/workflow · source` (model resolved per-turn). When the provenance hook is installed, the assistant stamps this; otherwise fill what you know. Append `scope: framework` only when this is framework-level feedback captured inside an active project (Q2, pending ratification); the default `scope: project` need not be written.
- **Inline-doc feedback:** annotate any document with a **single line** beginning `FU:` (or `DEC:` for a decision), e.g. `FU: this section needs a diagram`. One line per marker — for longer or multi-paragraph feedback, use chat, where your full text is captured verbatim. When the assistant reads the doc it harvests each marker with `Source: inline-doc` + `path#heading-anchor` (the nearest heading, edit-stable; a raw `:line` is a drift-prone fallback) and tells you in-turn what it captured. Before minting, it checks for an existing entry with the same `source: inline-doc` path/anchor **and identical text** — it skips only a true re-read (same location, same words); a marker whose **text changed** at that location is new feedback and gets a **new entry** (`Related:` the old id), so an in-place edit is never silently dropped (FM-001 / DA-002-i8 — no doc is mutated).
- On any conflict, **verbatim wins** (secrets/PII excepted — redact before capture, LOG-M-002). Corrections are append-only (convention-only, git-backstopped — not a filesystem lock): to fix a verbatim or reopen a `DONE`, add a new entry referencing the old id.

## Segment Index

**Rotate at the cap:** seal this ACTIVE file and start a new segment at **~50 entries or ~800 lines** (whichever first) — ids continue monotonically; see the walkthrough in `examples-appendix.md` and LOG-M-006. (The cap is restated here so it is legible from the log alone, independent of whether the rule file is loaded — PM-002-iter8.)

Segment files are enumerable by `ls`; the id-ranges are read from each segment's first/last headings. One row per segment; the ACTIVE row is this file.

| Segment | File | Canonical ids |
|---------|------|---------------|
| 1 | FEEDBACK-LOG.md (ACTIVE) | FU.0 – … |

> **Forward-nav (travels with this file):** from a sealed segment N, open `FEEDBACK-LOG.{N+1:03d}.md` if it exists, else the stable ACTIVE `FEEDBACK-LOG.md`. A sealed segment's `next:` may name a not-yet-created successor — the ACTIVE file is always the tail. **Backward-nav:** follow `prev:`.

---

## FU.0 commit-push-cadence (alias: FU.0)

> Worked example (genericized from a real standing directive). Note the `(alias: FU.0)` suffix — you typed `FU.0`, and here it happens to match the canonical id; on a later turn your `FU.0` would map to canonical `FU.1`, `FU.2`, and so on. Delete this block when real entries land.

**Verbatim:**
> Don't forget to commit and push to the remote on a regular cadence so that we benefit from the ability to be able to rollback or go back to a previous commit.

**Summary:** Standing directive — commit and push to `origin` at a regular cadence (milestone / workflow / phase boundaries) so rollback points exist.

**Disposition:** **DONE (standing — applies continuously).** Evidence: commits `<hash-a>` + `<hash-b>` pushed to `origin/<branch>`; memory `feedback-commit-push-cadence`.

**Context:** datetime `{YYYY-MM-DD}` · session `{session_id}` · model(s) `{model-per-turn}` · turn `{session_id}#{promptId}` (turn `{N}`) · agents/workflow `—` · source `chat`

<!-- inline-doc entries append the annotation location to source, e.g. `source inline-doc {path}:{line-or-anchor}` -->


---

## Backfill Queue

Feedback given before this log existed (candidates for retroactive entries, pending user authorization). Not a parking lot: rows carry an added-date and are reviewed at the same commit-cadence checkpoint as OPEN entries — **capped at the next milestone or ~3 months, whichever first** — promoted to a full entry or explicitly declined — and sooner if a row's source (memory/transcript) is observed to have rotated. On promotion, the item is tail-appended with the next canonical id (historical date in the body); the queue does not renumber existing ids. Every promoted backfill entry is tagged `(backfilled)` until an independent reference (commit hash, transcript pointer, memory key) is cited in it.

| Approx date | Added | Item | Source |
|---|---|---|---|
| {YYYY-MM-DD} | {YYYY-MM-DD} | {short description} | {chat / inline-doc / memory} |
