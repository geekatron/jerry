# Hook Design Note — Feedback/Decision Log Provenance Capture

> **Design-only.** No framework path is touched by this note. Installing any hook is a separate, gated step (touches `hooks/` + `src/interface/cli/hooks/`). Grounded in `research/feedback-decision-log-research.md §B.1, §B.3, §B-metadata`.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Principle](#principle) | Why harness-executed capture |
| [Seam 1: Provenance Sidecar](#seam-1-provenance-sidecar-userpromptsubmit) | Deterministic metadata stamp |
| [Seam 2: Capture Reminder](#seam-2-capture-reminder-stop--precompact) | Reminder / skeleton injection |
| [What the hook must NOT do](#what-the-hook-must-not-do) | Scope guardrails |
| [Fail-open contract](#fail-open-contract) | House-style safety |

## Principle

What depends on the model remembering will eventually be forgotten. Every field the harness can stamp deterministically (session id, timestamp, model-per-turn, turn ordinal, project id, transcript path) SHOULD be stamped by a fail-open hook; only judgment fields (which text is feedback, the summary, the disposition) remain model/human-authored. This directly attacks the [internal-kb] drift class (`DJ-025` id collision; hand-typed `session (2026-06-10 …)` prose labels).

## Seam 1: Provenance Sidecar (`UserPromptSubmit`)

Reuses the existing precedent `hooks_prompt_submit_handler.py` (already reads `transcript_path`, returns `additionalContext`).

- **On each user prompt**, write/append a sidecar record to Jerry session state, keyed `{session_id}#{promptId}`:
  `{ turn_ordinal, timestamp, model_of_last_assistant_turn, project_id, transcript_path, cwd, gitBranch }`.
- `turn_ordinal` is a harness-owned monotonic counter (the human-facing "turn N").
- `model_of_last_assistant_turn` is resolved by reading the last `assistant` record's `message.model` from the transcript JSONL (`[INFERENCE]`: model is not on hook stdin; it is only in the transcript — `research §B.1` finding 2).
- **When an entry is minted**, its Context line references the sidecar key instead of hand-typing metadata → provenance becomes harness-guaranteed.

## Seam 2: Capture Reminder (`Stop` / `PreCompact`)

- **`Stop`** — if the just-completed user turn matched feedback-signal heuristics (correction/preference/directive keywords: "no", "actually", "instead", "I want", "I'd like", "from now on", "don't", "stop"), emit a lightweight reminder ("unlogged feedback candidate this turn — append to FEEDBACK-LOG?") or inject a **pre-stamped skeleton stub** (Context pre-filled from the sidecar; Verbatim/Summary/Disposition left blank for the model/human to complete).
- **`PreCompact`** — imminent context loss; emit a stronger reminder to flush any pending feedback/decision entries before compaction. `PreCompact` already receives `transcript_path` + `session_id` (`research §B.1`).

## What the hook must NOT do

- MUST NOT classify which user text is "feedback" and auto-write a Verbatim/Summary/Disposition (judgment fields — `research §B-metadata`).
- MUST NOT block, delay, or fail a turn.
- MUST NOT write into the log body autonomously beyond an explicit, opt-in skeleton stub.
- MUST NOT invent a model or session value — only stamp what the transcript/stdin actually carries.

## Fail-open contract

Every handler swallows parse errors and continues (house style, `research §B.1` finding 4; `Stop`/`SubagentStop` wrappers even print `{"decision":"approve"}` on exception). A capture hook MUST be fail-open: a logging failure never costs the user a turn. Absent the hook, the MEDIUM rule (LOG-M-001..005) still governs manual capture — the hook only makes the durable path automatic.

## Feasibility verdict

**Feasible and low-risk** for Seam 1 (sidecar stamp) and Seam 2 (reminder) — both reuse fields the research proved are on hook stdin (`session_id`, `transcript_path`) plus a transcript read for model/turn. Recommended as a **fast follow** to the manual convention unless the user wants it in v1 ([design Q3]).
