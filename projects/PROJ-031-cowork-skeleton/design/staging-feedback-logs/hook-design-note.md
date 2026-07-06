# Hook Design Note — Feedback/Decision Log Provenance Capture

> **Design-only.** No framework path is touched by this note. Installing any hook is a separate, gated step (touches `hooks/` + `src/interface/cli/hooks/`). Grounded in `research/feedback-decision-log-research.md §B.1, §B.3, §B-metadata`. The lowercase "must"/"must not" below are **code-implementation constraints** for the (separately gated) hook script, not Jerry HARD-rule-tier governance — they carry no MEDIUM/HARD tier weight and do not touch the 25/25 ceiling.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Principle](#principle) | Why harness-executed capture |
| [Seam 1: Provenance Sidecar](#seam-1-provenance-sidecar-userpromptsubmit) | Deterministic metadata stamp |
| [Seam 2: Capture Reminder](#seam-2-capture-reminder-stop--precompact) | Reminder / skeleton injection |
| [Seam 3: Segment-cap reminder](#seam-3-optional-segment-cap-reminder) | Rotation reminder (optional) |
| [What the hook must not do](#what-the-hook-must-not-do) | Scope guardrails |
| [Fail-open contract](#fail-open-contract) | House-style safety |
| [Feasibility verdict](#feasibility-verdict) | Ship timing (Q3 default) |

## Principle

What depends on the model remembering will eventually be forgotten. Every field the harness can stamp deterministically (session id, timestamp, model-per-turn, turn ordinal, project id, transcript path) SHOULD be stamped by a fail-open hook; only judgment fields (which text is feedback, the summary, the disposition) remain model/human-authored. This directly attacks the [internal-kb] drift class (`[legacy-fu-id]` id collision; hand-typed `session (2026-06-10 …)` prose labels).

## Seam 1: Provenance Sidecar (`UserPromptSubmit`)

Reuses the existing precedent `hooks_prompt_submit_handler.py` (already reads `transcript_path`, returns `additionalContext`).

- **On each user prompt**, write/append a sidecar record to Jerry session state, keyed `{session_id}#{promptId}`:
  `{ turn_ordinal, timestamp, model_of_last_assistant_turn, project_id, transcript_path, cwd, gitBranch }`.
- `turn_ordinal` is a harness-owned monotonic counter (the human-facing "turn N").
- `model_of_last_assistant_turn` is resolved by reading the last `assistant` record's `message.model` from the transcript JSONL (`[INFERENCE]`: model is not on hook stdin; it is only in the transcript — `research §B.1` finding 2).
- **When an entry is minted**, its Context line references the sidecar key instead of hand-typing metadata → when the stamp is present, provenance is **harness-sourced** rather than hand-typed (subject to the fail-open contract below — a hook failure omits the stamp, never blocks the turn).

## Seam 2: Capture Reminder (`Stop` / `PreCompact`)

- **`Stop`** — if the just-completed user turn matched feedback-signal heuristics — correction/preference/directive keywords ("no", "actually", "instead", "I want", "I'd like", "from now on", "don't", "stop") **or interrogative/challenge patterns that frequently carry implicit feedback** ("why…", "what about…", "should we…", "what if…", "have you considered…", "wouldn't it be better…") — emit a lightweight reminder ("unlogged feedback candidate this turn — append to FEEDBACK-LOG?") or inject a **pre-stamped skeleton stub** (Context pre-filled from the sidecar; Verbatim/Summary/Disposition left blank for the model/human to complete).
  - **Disclosed residual (best-effort, non-exhaustive):** the keyword/pattern list is a *reminder trigger*, not a classifier — it **cannot** catch every phrasing (e.g. a real project entry, FU.9, was an interrogative that an earlier keyword-only list would have missed). This is acceptable because **capture does not depend on the hook**: LOG-M-001 (same-turn manual append) governs regardless; the hook only reduces the chance of a *forgotten* capture. A miss costs a reminder, never an entry.
- **`PreCompact`** — imminent context loss; emit a stronger reminder to flush any pending feedback/decision entries before compaction. `PreCompact` already receives `transcript_path` + `session_id` (`research §B.1`).

## What the hook must not do

- must not classify which user text is "feedback" and auto-write a Verbatim/Summary/Disposition (judgment fields — `research §B-metadata`).
- must not block, delay, or fail a turn.
- must not write into the log body autonomously beyond an explicit, opt-in skeleton stub.
- must not invent a model or session value — only stamp what the transcript/stdin actually carries.

## Fail-open contract

Every handler swallows parse errors and continues (house style, `research §B.1` finding 4; `Stop`/`SubagentStop` wrappers even print `{"decision":"approve"}` on exception). A capture hook must be fail-open: a logging failure never costs the user a turn. Absent the hook, the MEDIUM rule (LOG-M-001..006) still governs manual capture — the hook only makes the durable path automatic.

## Seam 3 (optional): segment-cap reminder

FU.5 introduces segment rotation at ~50 entries / ~800 lines. A hook MAY emit a **reminder** when the ACTIVE log crosses the cap ("FEEDBACK-LOG at 800+ lines — rotate to a new segment"). It must not rotate autonomously: sealing/creating segment files is a content operation with git implications, so it stays operator/assistant-driven. The reminder reuses the same fail-open shape as Seam 2. Anti-bloat: this is a reminder only, not a rotation engine.

## Feasibility verdict

**Feasible and low-risk** for Seam 1 (sidecar stamp) and Seam 2 (reminder); Seam 3 is a trivial size check. All reuse fields the research proved are on hook stdin (`session_id`, `transcript_path`) plus a transcript read for model/turn.

**PROPOSED-DEFAULT (Q3, pending ratification):** the hook is **designed in v1** (this note) but **shipped as a separate gated change** (it touches `hooks/` + `src/interface/cli/hooks/`, its own AE-002 gate). The manual MEDIUM convention (LOG-M-001..006) governs capture until the hook lands; the hook only makes the durable path automatic.
