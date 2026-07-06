# FEEDBACK-LOG — {SCOPE}

> Feedback / Follow-Up (FU) log. Captures user feedback and follow-up items **verbatim** with disposition tracking. Per the Feedback & Decision Log Standards (`feedback-decision-logs-standards.md`).
> **Scope:** project-scoped (`projects/<PROJECT_ID>/`) when a Jerry Project is active; repo-root otherwise.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Log Conventions](#log-conventions) | Entry schema |
| [FU.0 example-entry](#fu0-example-entry) | Worked example (delete when real entries land) |
| [Backfill Queue](#backfill-queue) | Pre-log feedback pending retro-capture |

## Log Conventions

Each entry records: **Verbatim** (user's exact words, typos preserved — verbatim means verbatim), **Summary** (assistant normalization), **Disposition** (`OPEN / IN-PROGRESS / DONE / WONTFIX` + evidence link on terminal states), **Context** (`datetime · session · model(s) · turn · agents/workflow · source`), and **Source** (`chat | inline-doc | transcript`).

- Ids are `FU.N`, monotonic within this file, never reset (start at `FU.0`). Global reference: `<scope>:FU.N`.
- Turn ref = `{session_id}#{promptId}` (machine anchor) + harness "turn N" (human-facing). Fall back to `{session_id}@{timestamp}` for inline-doc annotations.
- On any conflict, **verbatim wins**.

---

## FU.0 example-entry

**Verbatim:**
> {paste the user's exact words here, full, unedited — preserve typos and casing}

**Summary:** {1–3 sentence assistant normalization of what the user asked for. Never replaces the verbatim above.}

**Disposition:** **OPEN** {→ IN-PROGRESS → DONE (evidence link) / WONTFIX (reason). Add `Gating:` if this blocks a downstream step.}

**Context:** datetime `{YYYY-MM-DD}` · session `{session_id}` · model(s) `{model-per-turn}` · turn `{session_id}#{promptId}` (turn `{N}`) · agents/workflow `{ids or —}` · source `chat`

**Source detail (inline-doc only):** `{path}:{line-or-anchor}`

---

## Backfill Queue

Feedback given before this log existed (candidates for retroactive entries, pending user authorization):

| Approx date | Item | Source |
|---|---|---|
| {YYYY-MM-DD} | {short description} | {chat / inline-doc / memory} |
