# Examples Appendix — Feedback & Decision Logs

> Worked examples for the Feedback & Decision Log convention (per FU.8). The rule file (`feedback-decision-logs-standards.md`) stays lean and **points here** instead of embedding these.
> Examples are **drawn from this project's real entries, lightly genericized** — session ids and hashes shown as placeholders. **Canonical ids and `(alias: …)` values are illustrative** — constructed to demonstrate the id/alias mechanism (e.g. the standing directive is shown mid-log as `FU.3`, and the log-growth item as `FU.7`, with aliases assigned to teach the restart behavior), *not* transcribed verbatim from the live bootstrap logs (which currently hold `FU.0–FU.4` with no alias suffixes — see the note under Ids & aliases). Public-repo hygiene: no employer references, no absolute paths.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Ids & aliases (before / after)](#ids--aliases-before--after) | How logger-assigned ids relate to operator labels |
| [FEEDBACK-LOG worked examples](#feedback-log-worked-examples) | A standing DONE directive + an IN-PROGRESS item |
| [LLM-DECISION-LOG worked example](#llm-decision-log-worked-example) | A ratified decision with excerpt + pointer |
| [Segment rotation walkthrough](#segment-rotation-walkthrough) | Capped-collection linked-list in practice |
| [Evidence-link formats](#evidence-link-formats) | What a valid terminal-disposition evidence looks like |
| [Common cases](#common-cases) | Three questions the schema does not answer inline |

---

## Ids & aliases (before / after)

The operator **never tracks a global counter.** They label feedback however they like — usually restarting at `FU.0` every turn and every reviewed document. The **logger (LLM) assigns the canonical id**; the operator's label is recorded verbatim as an `alias`.

```
Turn 1 — operator types:  "FU.0 … FU.1 … FU.2 …"
Turn 2 — operator types:  "FU.0 … FU.1 …"          (restarted — normal habit)
Inline doc review — types: "FU.0 … FU.1 …"          (restarts again, per document)

Logger records (monotonic across the whole log, across segments, never resets):
  FU.0  (alias: FU.0)     FU.1  (alias: FU.1)     FU.2  (alias: FU.2)     ← turn 1
  FU.3  (alias: FU.0)     FU.4  (alias: FU.1)                              ← turn 2
  FU.5  (alias: FU.0)     FU.6  (alias: FU.1)                              ← inline doc
```

Same rule for `DEC-LLM-NNN`. The heading suffix carries the alias: `## FU.5 <slug> (alias: FU.0)`.

*(These ids/aliases are illustrative: the project's live bootstrap logs (FU.0–FU.4) contain no real alias collision yet, so this mechanism is exercised here synthetically, not against already-collided data.)*

---

## FEEDBACK-LOG worked examples

### Example 1 — a standing DONE directive

```markdown
## FU.3 commit-push-cadence (alias: FU.0)

**Verbatim:**
> Don't forget to commit and push to the remote on a regular cadence so that we
> benefit from the ability to be able to rollback or go back to a previous commit.

**Summary:** Standing directive — commit and push to `origin` at a regular cadence
(milestone / workflow / phase boundaries) so rollback points exist.

**Disposition:** **DONE (standing — applies continuously).** Evidence: commits
`<hash-a>` + `<hash-b>` pushed to `origin/<branch>`; memory `feedback-commit-push-cadence`.

**Context:** datetime `2026-07-05` · session `{session_id}` · model(s) `{model}` ·
turn `{session_id}#{promptId}` (turn `{N}`) · agents/workflow `—` · source `chat`
```

*Why it is shaped this way:* the verbatim is full and unedited; the Summary normalizes; the terminal `DONE` carries an evidence link (LOG-M-002, lint check 3). A standing directive stays `DONE` and is re-applied continuously.

> **Same entry, two positions (why the id differs from the template).** `FEEDBACK-LOG.template.md` shows this same standing directive as a *fresh log's first entry*, canonical `FU.0`. Here it sits **mid-log as canonical `FU.3`** while the operator's alias stays `FU.0`. That is the point: the **alias is stable, the canonical id advances with log position** — the two are deliberately not required to match.

### Example 2 — an IN-PROGRESS item (shows the alias restart)

```markdown
## FU.7 log-growth-capped-collection (alias: FU.0.1)

**Verbatim:**
> …The design sounds like an append only log, which makes me wonder, what are the
> consequences… when this file grows too large?… Should we be treating this more
> like a capped collection… treat this like a linked-list so that it's easy to
> navigate forward and backwards between the decision and feedback logs.

**Summary:** Append-only logs will exceed LLM read limits; adopt capped-collection
segment rotation with linked-list prev/next navigation and a segment index.

**Disposition:** **IN-PROGRESS** — folded into the design revision (segment rotation added).

**Context:** datetime `2026-07-05` · session `{session_id}` · model(s) `{model}` ·
turn `{session_id}#{promptId}` (turn `{N}`) · agents/workflow `fu-log-convention-…` · source `chat`
```

*Note the alias:* the operator labelled this `FU.0.1` (their per-turn restart); the logger assigned canonical `FU.7` — simply the **next free id after `FU.6`** from the ids/aliases block above (canonical ids advance monotonically regardless of what the alias says).

---

## LLM-DECISION-LOG worked example

```markdown
## DEC-LLM-001 ratify-approach-b (alias: —)

**Decision:** Approach **B** (subject-encoded identity) is ratified as canonical; the
load-bearing "promotion-is-the-point" assumption is confirmed by the user (P-020).

**User verbatim:**
> See FEEDBACK-LOG FU.0    (single-sourced there; or paste the full user text)

**Assistant verbatim (decision-relevant excerpt):**
> "The trade study proved the winner turns entirely on one belief: baseline weights →
> the two-namespace option wins; promotion-is-normal weights → B wins. The evidence for
> 'promotion is normal' is that it is literally the framework's thesis, and 100% of
> existing ADRs reached their home via promotion. I recommend ratifying B — but it is
> your framework-trajectory call."
(Full turn: transcript `{session_id}#{uuid}`.)

**Summary / consequences:** B canonical for all new ADRs; the prior project-scoped dialect
is grandfathered in place; bare ids deprecated for new ADRs; MEDIUM-tier enforcement only.

**Context:** datetime `2026-07-05` · session `{session_id}` · model `{model}` ·
agents/workflow `{workflow_id}` · artifacts `decisions/ADR-<domain-slug>-NNN.md` ·
Reflected in `ADR-<domain-slug>-NNN`
```

*Why user-verbatim-full but assistant-excerpt+pointer:* user turns are short and authoritative → kept full (or single-sourced to the FEEDBACK-LOG). Assistant turns run 3k–15k tokens → an excerpt plus a `{session_id}#{uuid}` transcript pointer keeps the log loadable; the full turn stays recoverable from the JSONL **while that transcript is retained and its pointer resolves** (an unenforced dependency — design doc Q1; the C3+ full-paste option is the mitigation). (PROPOSED-DEFAULT — pending Q1 ratification; full paste optional for C3+/ADR-graduating decisions.)

---

## Segment rotation walkthrough

When the ACTIVE `FEEDBACK-LOG.md` first reaches **~50 entries or ~800 lines**, seal it and start a fresh ACTIVE. Canonical ids continue — they never reset.

```
Before rotation:
  FEEDBACK-LOG.md          ← Segment 1 (ACTIVE)   FU.0 … FU.49   prev: —   next: —

After rotation (FU.49 crossed the cap):
  FEEDBACK-LOG.001.md      ← Segment 1 (SEALED)   FU.0 … FU.49
                             header: Segment 1 · prev: — · next: FEEDBACK-LOG.002.md
  FEEDBACK-LOG.md          ← Segment 2 (ACTIVE)   FU.50 …
                             header: Segment 2 · prev: FEEDBACK-LOG.001.md · next: —
```

**Segment Index** (lives in the ACTIVE file; one row per segment):

```markdown
| Segment | File | Canonical ids |
|---------|------|---------------|
| 1 | FEEDBACK-LOG.001.md | FU.0 – FU.49 |
| 2 | FEEDBACK-LOG.md (ACTIVE) | FU.50 – … |
```

**Forward-nav rule:** from segment N, go to `FEEDBACK-LOG.{N+1:03d}.md` if it exists, else the ACTIVE `FEEDBACK-LOG.md`. **Backward-nav:** follow `prev`. **Cross-log:** an FU entry that cites `DEC-LLM-012` needs no path — the LLM-DECISION-LOG's own Segment Index resolves `DEC-LLM-012 → which segment file`. Ids are the join key; rotation never breaks a cross-reference.

The `LLM-DECISION-LOG` rotates identically (`LLM-DECISION-LOG.001.md`, …).

---

## Evidence-link formats

Terminal dispositions (`DONE` / `WONTFIX`) carry an evidence link **or** a one-line reason. Evidence is intentionally free-form — any of these is valid:

```
Evidence: commit `<hash>` pushed to `origin/<branch>`
Evidence: projects/PROJ-031-cowork-skeleton/decisions/ADR-<domain-slug>-NNN.md
Evidence: DEC-LLM-004
Evidence: STORY-012 (graduated to worktracker)
Reason (WONTFIX): superseded by FU.9; no longer applicable.
```

The L5 lint asserts an evidence link **or** reason is *present* — not its exact shape (over-fitting the format would be machinery).

---

## Common cases

- **I forgot to capture feedback this turn.** Add it later as a normal entry, or drop it in the **Backfill Queue** (candidate row); promote to a full entry when authorized.
- **I annotated the same `FU:` line in a doc that gets read more than once.** The assistant records the marker's location as `source: inline-doc <path>#<nearest-heading-anchor>` — a heading anchor, not a raw line number, so the key survives edits above it (FM-002-i008fmea). Example Context sub-field: `source inline-doc research/pricing-options.md#tam-sam-som`. Before minting, it checks for an existing entry carrying that same `path#anchor` **and the same text**; an unchanged marker already logged is not re-captured (FM-001). **If you edited the marker in place (same line, new wording), that is new feedback — the assistant mints a new entry for the changed text and links it `Related:` the old id, rather than skipping it as a duplicate (DA-002-i8).** No `<!-- HARVESTED -->` comment is written back into your document.
- **"What's the status of FU.0?" (a bare back-reference).** A bare token maps to several ids. Do **not** guess from recency — the assistant enumerates candidates on **both axes**: entries whose *alias* is `FU.0` (e.g. `FU.0 (alias: FU.0)`, `FU.3 (alias: FU.0)`, `FU.5 (alias: FU.0)`) **and** whether `FU.0` is itself a live *canonical* id (a distinct candidate), **listing each candidate's source (its document/turn)** so entries from unrelated docs that reused `FU.0` are distinguishable, then asks which is meant (H-31 / FM-008). Any disambiguating context you give ("three turns ago", a topic word) is used to narrow the list first. Referencing the canonical `FU.N` avoids the round-trip.
- **How do I find "that feedback about X"?** Use the **Segment Index** to pick the segment, then `grep` the slug / `Disposition: OPEN`. No tagging system needed.
- **The verbatim was transcribed wrong / a DONE item must reopen.** The log is append-only. Add a **follow-up entry** that references the old canonical id and corrects or reopens it; the original verbatim stays as the fidelity record. Add a `Superseded by: FU.N` line to the old entry (a status pointer, like a disposition update — not a verbatim change) so a later reader following a stale cross-reference is routed forward.
- **I'm editing the log by hand with no assistant in the loop.** Mint the next canonical id yourself: read the last `## FU.N` / `## DEC-LLM-NNN` heading in the ACTIVE file and use `N+1` — single-writer discipline still applies **provided no other session/window or agent is also appending to this log** (if one is, you are *not* the single writer and this is an undefended last-write-wins race; LOG-M-005). *If the ACTIVE file was just rotated and holds no entry yet, take the highest id in the Segment Index's id-range and add 1. If the file is at or near the segment cap, derive the next id as *the segment's starting id (from its Segment-Index row) + a `grep -c '^## FU\.'` count* — the bare count is file-local, not the global id, so the offset is needed in every segment after the first (DA-001-iter7) — rather than a Read that may truncate before the tail (PM-002).* Once the Q3 provenance hook ships, this becomes harness-assisted; until then it is a manual one-step lookup.
