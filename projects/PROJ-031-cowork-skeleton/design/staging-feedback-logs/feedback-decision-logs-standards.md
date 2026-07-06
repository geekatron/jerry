# Feedback & Decision Log Standards

> Two append-only ledgers so user feedback and human↔LLM decisions survive compaction, sessions, and model swaps. MEDIUM tier (HARD ceiling is full at 25/25). Fail-open hook assists; nothing auto-closes.

## Document Sections

| Section | Purpose |
|---------|---------|
| [MEDIUM Standards](#medium-standards) | LOG-M-001..005 |
| [FEEDBACK-LOG](#feedback-log) | Schema, id, triggers, disposition |
| [LLM-DECISION-LOG](#llm-decision-log) | Schema, verbatim policy, boundary |
| [Scoping](#scoping) | Project-scoped vs repo-root |
| [L5 Lint](#l5-lint) | Three cheap checks |
| [Boundaries](#boundaries) | DEC-NNN, ADR, H-32 |

## MEDIUM Standards

> SHOULD-tier. Override requires documented justification.

| ID | Standard |
|----|----------|
| LOG-M-001 | Feedback SHOULD be appended to the scoped FEEDBACK-LOG in the **same turn** it is given — from chat **or** inline-document annotations. |
| LOG-M-002 | User feedback SHOULD be captured **verbatim and full** (typos preserved). On any conflict between verbatim and a summary, **verbatim wins**. |
| LOG-M-003 | Decision-bearing exchanges SHOULD be appended to the scoped LLM-DECISION-LOG: user verbatim full; assistant verbatim per the ratified policy (excerpt + transcript pointer). |
| LOG-M-004 | Log entries SHOULD **cross-link, never duplicate** worktracker `DEC-NNN` / ADRs. A hardened, work-item-attached decision **graduates** into a DECISION entity and/or ADR. |
| LOG-M-005 | Ids SHOULD be **file-monotonic** (`FU.N`, `DEC-LLM-NNN`); provenance SHOULD reference the harness sidecar rather than hand-typed session/model values. |

## FEEDBACK-LOG

Entry = `## FU.N <slug>` (N monotonic per file, never resets; starts at `FU.0`). Global reference: `<scope>:FU.N`.

Fields (fixed order):
- **Verbatim** — user's exact words, always full, blockquoted.
- **Summary** — assistant normalization (1–3 sentences); never replaces the verbatim.
- **Disposition** — `OPEN / IN-PROGRESS / DONE / WONTFIX`. Terminal states carry an evidence link (commit/file/`DEC-LLM-NNN`/worktracker id/ADR) or a one-line reason. Optional `Gating:` note.
- **Context** — `datetime · session · model(s) · turn · agents/workflow · source`. Model resolved per-turn (may vary within a session).
- **Source** — `chat | inline-doc | transcript`. For `inline-doc`: file path + line/anchor.

**Capture triggers** — append when the user (1) corrects/overrides/redirects, (2) states a preference or standing instruction, (3) gives a follow-up item or ruling, or (4) annotates a document inline (harvest on read with `Source: inline-doc`).

## LLM-DECISION-LOG

Entry = `## DEC-LLM-NNN <slug>` (NNN monotonic per file). Fields:
- **Decision** — one sentence.
- **User verbatim** — full (short, authoritative). Single-source from FEEDBACK-LOG when it already lives there.
- **Assistant verbatim** — decision-relevant excerpt + transcript pointer `{session_id}#{uuid}` (full turn recoverable from the JSONL).
- **Summary / consequences**.
- **Context** — `datetime · session · model · agents/workflow · artifacts`.

## Scoping

`JERRY_PROJECT` set → `projects/<PROJECT_ID>/{FEEDBACK-LOG,LLM-DECISION-LOG}.md`. Unset → repo-root `{FEEDBACK-LOG,LLM-DECISION-LOG}.md`. Both logs use the same rule.

## L5 Lint

Cheap, fail-fast, pure-text. Maximum three:
1. **Nav table** — each log file > 30 lines has a nav table (H-23, scoped to these filenames).
2. **Id integrity** — `FU.N` / `DEC-LLM-NNN` ids are unique and strictly increasing within each file.
3. **Terminal evidence** — every `DONE` / `WONTFIX` entry has an evidence link or a reason line.

## Boundaries

- **Worktracker `{ParentId}:DEC-NNN`** — work-item-scoped, AST-validated (H-33), state-machine, wins on conflict. The log is the low-ceremony ledger that **precedes and graduates into** it; the log entry is never itself a DECISION entity.
- **ADR** — a ratified, durable decision graduates to a Scheme-B ADR (`ADR-{domain-slug}-NNN`) with a bidirectional cross-link.
- **H-32 (GitHub parity)** — does **not** apply per log entry (too heavy for turn-by-turn). Parity attaches only after an item graduates into a worktracker Story/Bug/Enabler.
