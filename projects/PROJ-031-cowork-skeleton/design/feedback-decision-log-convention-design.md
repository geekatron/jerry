# Design: FEEDBACK-LOG + LLM-DECISION-LOG Jerry Convention

> **PS Context:** PROJ-031-cowork-skeleton · ps-architect (convergent, opus) · Design for user requirement **FU.2** (2026-07-05).
> **Status:** DRAFT for user sign-off. P-020: nothing here writes into framework paths; all artifacts land under `projects/PROJ-031-cowork-skeleton/`. Install is AE-002/AE-003 auto-C3 (adversary gate) **after** approval.
> **Inputs:** `research/feedback-decision-log-research.md` (verbatim [internal-kb] rules + Jerry automation inventory), the two bootstrap logs (`FEEDBACK-LOG.md`, `LLM-DECISION-LOG.md`), `.context/rules/quality-enforcement.md` (HARD ceiling 25/25 → this convention MUST be MEDIUM-tier), `.context/rules/markdown-navigation-standards.md` (H-23).
> **Method:** Direct extraction. Quotes carry paths; inference is labelled `[INFERENCE]`.

## Navigation

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | What we are building and the 5 improvements over [internal-kb] |
| [L1: Full Design](#l1-full-design) | Schemas, id scheme, capture triggers, scoping, automation |
| [L1.1 FEEDBACK-LOG](#l11-feedback-log) | Entry schema, id scheme, disposition, triggers, scoping |
| [L1.2 LLM-DECISION-LOG](#l12-llm-decision-log) | Entry schema, verbatim tradeoff, DEC/ADR boundary, scoping |
| [L1.3 Automation](#l13-automation-hook-assisted-capture) | Automatable metadata + hook-assisted design (design-only) |
| [L2: Governance & Migration](#l2-governance--migration) | MEDIUM rule file, L5 lint, H-32 interplay, adoption plan |
| [Improvement Ledger](#improvement-ledger-vs-internal-kb) | Per-item [internal-kb]→Jerry rationale |
| [Open Questions For User](#open-questions-for-user) | Max 4 — only questions that change the design |
| [Staged Artifacts](#staged-artifacts) | Drafts ready to install post-approval |
| [References](#references) | Source paths |

---

## L0: Executive Summary

We are turning an un-codified, entirely-manual [internal-kb] pattern into a real, lightweight Jerry convention: **two append-only markdown ledgers** that guarantee user feedback and human↔LLM decisions survive context compaction, session boundaries, and model swaps.

- **FEEDBACK-LOG** captures every user feedback / follow-up item **verbatim** (typos preserved) with an assistant summary, a 4-state disposition (`OPEN / IN-PROGRESS / DONE / WONTFIX`), and machine-stampable provenance (session, model-per-turn, turn anchor, source channel).
- **LLM-DECISION-LOG** captures every decision-bearing exchange: user verbatim (full) + assistant verbatim (excerpt + transcript pointer — see the ratification question), summary/consequences, and a crisp boundary to worktracker `DEC-NNN` and ADRs (cross-link, never duplicate).
- Both are **project-scoped when `JERRY_PROJECT` is set, else repo-root** (the user's decision-log scoping rule, applied symmetrically to both logs).

**The five improvements over [internal-kb]** (`research §L1.A` critique): (1) it becomes a **codified, shipped convention** (rule + templates) instead of an emergent wish (`OI-019` never shipped); (2) **file-monotonic ids** replace manual `R{round}-FU.{n}` numbering that already collided in the wild (`DJ-025`); (3) **harness-stamped provenance** replaces hand-typed model/session labels that drifted (`claude-opus-4-8` vs the prose label `session (2026-06-10 eng-arch reconciliation)`); (4) a **turn model** (composite anchor + hook-maintained ordinal) replaces manually-declared "rounds" that fit turn-by-turn chat poorly; (5) a **project/root scoping rule + inline-doc source channel** replaces the PDD-only binding.

**The governing principle (from the research):** *what depends on the model remembering will eventually be forgotten.* Every field the harness can stamp deterministically (session id, timestamp, model-per-turn, turn anchor) is designed to be stamped by a fail-open hook; only judgment fields (which text is feedback, the summary, the disposition) remain model/human-authored.

**Design posture: start minimal.** The staged rule file targets **≤ ~1,500 tokens** and **≤ 3** L5 lint checks — a deliberate correction of the ADR-convention over-engineering spiral (`staging/adr-standards-rule-draft.md` reached ~19k on disk; iteration-005 composite 0.66). Ship the smallest thing that makes "don't lose feedback" true, then grow only on evidence.

---

## L1: Full Design

### L1.1 FEEDBACK-LOG

#### Entry schema

Each entry is a `## FU.N <slug>` section with this body (fixed field order):

| Field | Content | Author | Rule |
|-------|---------|--------|------|
| **Verbatim** | User's exact words, **always full**, typos/casing preserved. Blockquoted. | user (copied) | MUST be word-for-word. The verbatim is the fidelity anchor: on any conflict, **verbatim wins**. |
| **Summary** | Assistant's normalization (1–3 sentences). | assistant | MUST NOT replace or "correct" the verbatim. |
| **Disposition** | One of `OPEN / IN-PROGRESS / DONE / WONTFIX`. Terminal states (`DONE`,`WONTFIX`) MUST carry an **evidence link** (commit / file / `DEC-LLM-NNN` / worktracker id / ADR) or a one-line reason. Optional `Gating:` note if the item blocks a downstream step. | assistant/human | Lifecycle is human-owned; nothing auto-closes. |
| **Context** | `datetime · session · model(s) · turn · agents/workflow · source`. | harness-stampable (see L1.3) | Model(s) resolved **per turn** from the transcript (may vary within a session). |
| **Source** | `chat` \| `inline-doc` \| `transcript`. For `inline-doc`: include file path + line/anchor of the annotation. | harness/assistant | New field ([internal-kb] had none). |

#### Id scheme (honors `FU.N. <slug>`, unique across sessions/projects)

- **Human id = `FU.N`**, where **N is monotonic within the log file and never resets** (starts at `FU.0` to honor the user's own 2026-07-05 `FU.0/1/2` labeling, which the bootstrap already uses). Slug follows in the heading.
- **Globally-unique reference = `<scope>:FU.N`** where `<scope>` is the project id (`PROJ-031:FU.2`) or `root` (`root:FU.5`). The file scope disambiguates across projects; monotonicity disambiguates within a file.
- **Machine anchor** (in Context) = composite `{session_id}#{promptId}` (fall back to `{session_id}@{timestamp}` when no promptId exists, e.g. an inline-doc annotation harvested later).
- **`[INFERENCE]` / design decision:** the user sometimes numbers `FU.0, FU.1…` *per message* (resetting). We treat that per-message numbering as a **display convenience recorded inside the verbatim**, not the canonical key. The log's `FU.N` is file-monotonic. This is the single fix that kills the [internal-kb] `R{round}-` prefix crutch and its observed collisions — see [Open Questions](#open-questions-for-user) Q4 if the user prefers per-message reset.

#### Capture triggers (when an entry MUST be written)

Per the MEDIUM rule (LOG-M-001), an entry SHOULD be appended **in the same turn** the feedback is given, whenever the user:

1. Corrects, overrides, or redirects the assistant ("no", "actually", "instead", "don't", "stop", "that's wrong").
2. States a preference or standing instruction that should change future behavior ("I want", "I'd like", "from now on", "always/never").
3. Provides a follow-up item or ruling on an open question.
4. **Annotates a document inline** with feedback (e.g. `>AN: FU.n. …`, review comments, or any inline directive). When the assistant *reads* a doc containing such annotations, it MUST harvest them into the log with `Source: inline-doc` + path + line.

The rule is **MEDIUM (SHOULD)** — it cannot be HARD (ceiling 25/25) — and is backed by a fail-open capture hook (L1.3) so the obligation does not depend on the model remembering.

#### Scoping

- `JERRY_PROJECT` set → `projects/<PROJECT_ID>/FEEDBACK-LOG.md`.
- `JERRY_PROJECT` unset → repo-root `FEEDBACK-LOG.md`.
- Symmetric with LLM-DECISION-LOG scoping (the user specified the rule for the decision log; we apply it to both for consistency). See [Open Questions](#open-questions-for-user) Q2 for the framework-level-feedback-during-a-project edge case.

### L1.2 LLM-DECISION-LOG

#### Entry schema

Each entry is a `## DEC-LLM-NNN <slug>` section (NNN monotonic within file):

| Field | Content | Author |
|-------|---------|--------|
| **Decision** | One sentence: what was decided. | assistant |
| **User verbatim** | User's exact words, **full** (user text is short and authoritative). If the user text already lives in FEEDBACK-LOG, single-source it there and link (`See FEEDBACK-LOG FU.N`). | user (copied) |
| **Assistant verbatim** | The **decision-relevant excerpt** (the recommendation / options / rationale / pushback) **+ a transcript pointer** `{session_id}#{uuid}` to the full turn. *(Default; see the ratification tradeoff below and Q1.)* | assistant |
| **Summary / consequences** | What follows from the decision; downstream effects. | assistant |
| **Context** | `datetime · session · model · agents/workflow · artifacts`. | harness-stampable |

#### The verbatim tradeoff (user asked for full; MUST be ratified)

The user requirement asks for *"your verbatim responses, my verbatim responses."* Assistant turns, unlike user turns, are large. Two options, with size math:

| Option | What the log stores | Size math (100 decisions) | Consequence |
|--------|--------------------|--------------------------|-------------|
| **A — full paste** | Entire assistant turn verbatim | Assistant turns run ~3k–15k tokens each → **~0.3M–1.5M tokens** in the log file | Literal compliance with the request, but the log becomes unloadable and **re-creates the context-rot problem Jerry exists to solve**. A single Read of the file would blow the context budget (violates CB-02/CB-05 spirit). |
| **B — excerpt + pointer** *(recommended default)* | Decision-relevant excerpt (~150–400 tokens) + `{session_id}#{uuid}` transcript pointer | **~15k–40k tokens** for the whole log; full turn always recoverable from the immutable JSONL transcript | Log stays lean and loadable; **full fidelity is preserved** (the transcript is the byte-exact source of record); pointer is harness-resolvable. This is the bootstrap's choice and the research recommendation. |

**Recommendation:** **Option B** as the ratified default — the transcript JSONL *is* the verbatim record; the log excerpts and points to it. This honors the intent (nothing is lost — the full turn is one pointer away) without defeating Jerry's core thesis. **But the user explicitly said "full," so this is a P-020 ratification question** ([Q1](#open-questions-for-user)). User verbatim stays full in both options (it is short).

#### Boundary to worktracker `DEC-NNN` and ADRs (cross-link, never duplicate)

The worktracker DECISION entity (`{ParentId}:DEC-NNN`, `.context/templates/worktracker/DECISION.md`) is *also* "for decisions between the User and Claude" (`research §B.2`) — a real overlap. Keep them distinct by **scope, ceremony, lifecycle**, connect by **graduation**:

| Dimension | LLM-DECISION-LOG (new) | Worktracker `{ParentId}:DEC-NNN` (exists) |
|-----------|----------------------|-------------------------------------------|
| Scope | Session/interaction-level; project-root **or** project-scoped | Work-item-scoped; **requires** Epic/Feature/Story/Enabler parent |
| Ceremony | Low; append-only ledger; provenance-first | High; `participants[]` required, co-located, **AST-validated (H-33)** |
| Lifecycle | Running capture (survives compaction) | State machine `PENDING→DOCUMENTED→ACCEPTED/SUPERSEDED` (terminal) |
| Authority on conflict | **Loses** to the formal artifact | **Wins** (ratified) |
| Id | `DEC-LLM-NNN` (distinct namespace) | `{ParentId}:DEC-NNN` |

**Boundary rule (LOG-M-004):** the LLM-DECISION-LOG is the **working provenance ledger**. When a decision hardens *and* attaches to a work item, it **graduates** into a worktracker DECISION and/or a Scheme-B ADR, with a bidirectional cross-link (`Reflected in:` here, `Source:` there). The log entry is **never itself** a DECISION entity (no parent, no state machine, no AST schema). The `DEC-LLM-` prefix guarantees the two id spaces can never collide.

#### Scoping

Identical rule to FEEDBACK-LOG: `projects/<PROJECT_ID>/LLM-DECISION-LOG.md` when `JERRY_PROJECT` set, else repo-root `LLM-DECISION-LOG.md` (this is the user's stated rule, verbatim FU.2).

### L1.3 Automation (hook-assisted capture)

#### What the harness can stamp deterministically (research §B-metadata)

| Field | Automatable? | Source |
|-------|-------------|--------|
| session id | **YES** | hook stdin `session_id` (SessionStart/PreCompact/SubagentStop) |
| transcript path | **YES** | hook stdin `transcript_path` |
| datetime | **YES** | transcript `timestamp` / system clock |
| project id + which log file | **YES** | `JERRY_PROJECT` env → selects project-scoped vs repo-root |
| cwd / gitBranch / CC version | **YES** | transcript fields |
| **model(s) per turn** | **YES, but only via transcript** | assistant record `message.model`; **not on hook stdin** `[INFERENCE]`; resolve per-turn (varies within a session) |
| turn reference | **YES (resolvable); no native number** | `{session_id}#{promptId}` + hook-maintained ordinal |
| agent id | **PARTIAL** | `SubagentStop` `agent_id`/`agent_transcript_path`; main-thread turns have none |
| verbatim / summary / disposition | **NO** | model/human judgment |

#### Hook-assisted design (design-only — no framework paths touched)

Principle: harness-executed capture is the durable path. Two fail-open seams, both reusing existing precedent (`hooks_prompt_submit_handler.py` already reads `transcript_path` and returns `additionalContext`):

1. **Provenance sidecar stamp (`UserPromptSubmit`)** — on each user prompt, write/append a small sidecar record keyed `{session_id}#{promptId}` to Jerry session state: `{turn_ordinal, timestamp, model_of_last_assistant_turn, project_id, transcript_path}`. When an entry is minted, its Context line **references the sidecar key** rather than hand-typing the metadata — this is what kills the `DJ-025`-class drift. Turn ordinal is a harness-owned monotonic counter (the human-facing "turn N").
2. **Capture reminder / skeleton injection (`Stop` and `PreCompact`)** — at `Stop`, if the just-completed user turn matched feedback-signal heuristics (correction/preference keywords), inject a lightweight reminder ("unlogged feedback candidate this turn — append to FEEDBACK-LOG?") or a pre-stamped **skeleton entry stub** (Context pre-filled, Verbatim/Summary/Disposition blank). At `PreCompact` (imminent context loss), inject a stronger reminder to flush any pending entries. Fail-open always (never block a turn because logging failed — house style, `research §B.1`).

**Scope control:** the hook only *stamps provenance and reminds*; it never classifies or writes verbatim/summary/disposition (those need judgment). This keeps the automation small and within what the research proved is on hook stdin. Whether the hook ships in v1 or as a follow-up is [Q3](#open-questions-for-user).

---

## L2: Governance & Migration

### MEDIUM-tier rule file

The HARD ceiling is **25/25 with zero headroom** (`quality-enforcement.md`), so a "MUST log" rule is impossible without a C4 ceiling-exception ADR. The convention ships as a **MEDIUM (SHOULD)** rule file — staged as `staging-feedback-logs/feedback-decision-logs-standards.md`, target **≤ ~1,500 tokens** — with these rule ids:

| Id | Standard (MEDIUM / SHOULD) |
|----|---------------------------|
| LOG-M-001 | Feedback SHOULD be appended to the scoped FEEDBACK-LOG in the same turn it is given (chat or inline-doc). |
| LOG-M-002 | User feedback text SHOULD be captured **verbatim and full**; verbatim wins on conflict. |
| LOG-M-003 | Decision-bearing exchanges SHOULD be appended to the scoped LLM-DECISION-LOG (user verbatim full; assistant per the ratified verbatim policy). |
| LOG-M-004 | Log entries SHOULD cross-link — never duplicate — worktracker `DEC-NNN` / ADRs; hardened decisions graduate. |
| LOG-M-005 | Ids SHOULD be file-monotonic (`FU.N`, `DEC-LLM-NNN`); provenance SHOULD reference the harness sidecar, not hand-typed values. |

### L5 lint candidates (cheap, ≤ 3)

Deliberately minimal — the ADR-convention failure was an 18-rule lint. Ship at most these three, all pure-text and fail-fast:

1. **Nav table present** — if `FEEDBACK-LOG.md` / `LLM-DECISION-LOG.md` exists and is > 30 lines, it MUST have a nav table (already H-23; the lint just scopes it to the log filenames).
2. **Id uniqueness + monotonicity** — `FU.N` / `DEC-LLM-NNN` ids in each file are unique and strictly increasing (catches the `DJ-025` collision class).
3. **Terminal disposition has evidence** — every `DONE`/`WONTFIX` entry has an evidence link or a reason line.

### H-32 interplay

Do **not** mandate a GitHub Issue per feedback item — turn-by-turn capture would flood the issue tracker and defeat low-friction logging. The log itself is **not** an H-32-tracked entity. H-32 attaches only **after graduation**: if a feedback item becomes a worktracker Story/Bug/Enabler, that entity gets GH parity as usual. The log is the internal SSOT that *precedes* formalization.

### Adoption / migration plan

1. **Approve this design** (user sign-off on the 4 open questions).
2. **Adversary gate** (AE-002/AE-003 auto-C3: install touches `.context/rules/` and adds an ADR) — blind review before any framework-path write.
3. **Install** (framework paths — separate authorized step, not this task): move `staging-feedback-logs/feedback-decision-logs-standards.md` → `.context/rules/`; register in CLAUDE.md skill/nav tables; add templates to `.context/templates/`; add the trigger to `mandatory-skill-usage.md` if a skill wraps it.
4. **Adopt the two bootstrap files in place** — `PROJ-031/FEEDBACK-LOG.md` and `LLM-DECISION-LOG.md` already encode the ratified schema (Disposition enum, scoping, DEC boundary, Backfill Queue). Migration = swap the "BOOTSTRAP format" banner for the ratified-convention banner; **entries and ids are preserved** (FU.0–FU.2, DEC-LLM-001..003 keep their numbers).
5. **Backfill** (optional, [Q4](#open-questions-for-user)) — the two Backfill Queues list pre-log items; adopt retroactively or leave forward-only.
6. **Hook** ([Q3](#open-questions-for-user)) — ship the provenance/reminder hook now or as a fast follow (its own gate; touches `hooks/`).
7. **ADR** — capture the whole convention as **`ADR-feedback-decision-logs-001`** (the first born-Scheme-B ADR; id already reserved in FEEDBACK-LOG FU.2 disposition and DEC-LLM-003).

---

## Improvement Ledger (vs [internal-kb])

Explicit per-item rationale, as required. `[M]` = [internal-kb] behavior (research §L1.A); `[J]` = this design.

| # | [internal-kb] `[M]` | Jerry `[J]` improvement | Why better |
|---|-----------------|------------------------|------------|
| 1 | Emergent, un-codified; zero rule/template refs; `OI-019` "templatize" never shipped | Codified MEDIUM rule + 2 templates + optional hook | The user's goal ("so that we don't lose feedback") requires enforcement, not a wish. |
| 2 | Manual `R{round}-FU.{n}`; `DJ-025` records an id collision | File-monotonic `FU.N` / `DEC-LLM-NNN` + `<scope>:` reference | Removes the round crutch and the observed collision class; survives background agents. |
| 3 | Hand-typed model/session (`claude-opus-4-8` vs prose `session (2026-06-10 …)`) | Harness-stamped provenance sidecar; model resolved per-turn from transcript | Kills exactly the metadata humans forget/mistype; handles mid-session model swaps (`claude-opus-4-8`→`claude-fable-5`). |
| 4 | "Rounds" (manual review-pass grouping) | Turn model: `{session_id}#{promptId}` + hook ordinal | Fits the user's turn-by-turn requirement, which rounds model poorly. |
| 5 | PDD-artifact-bound only | Project-scoped-or-root + `Source: chat\|inline-doc\|transcript` | Matches the user's scoping rule and the inline-doc capture requirement. |
| 6 | 5-state legend (Addressed/In progress/Planned/Deferred/Gating) | 4-state enum + orthogonal `Gating:` note; evidence required on terminal | Simpler lifecycle; "gating" is a flag, not a state; closure is auditable. |
| 7 | Full verbatim implied; no size discipline | Excerpt + transcript pointer (Option B) with size math + P-020 ratification | Preserves fidelity via the immutable transcript without re-creating context rot. |
| 8 | Journal vs `decisions.md` boundary informal | Formal boundary table + `DEC-LLM-` namespace + graduation rule; protects H-33 worktracker DECISION | Prevents shadowing the AST-validated DECISION entity. |

---

## Open Questions For User

> Only questions that change the design. Max 4.

1. **Assistant-verbatim length policy (P-020 ratification).** You asked for *full* assistant verbatim. Full paste = ~0.3M–1.5M tokens over 100 decisions (log becomes unloadable, re-creates context rot). **Recommended: Option B — decision-relevant excerpt + `{session_id}#{uuid}` transcript pointer** (~15k–40k total; full turn always recoverable from the immutable JSONL). Ratify **A (full)** or **B (excerpt+pointer)**? *(User verbatim stays full either way.)*
2. **Framework-level feedback during an active project.** When `JERRY_PROJECT` is set, all feedback defaults to the project log. Some feedback is framework-level (about Jerry itself, not the project). Route such items to **(a)** the active project log with a `scope: framework` tag, or **(b)** always the repo-root log regardless of active project? *(Changes routing logic.)*
3. **Automation timing.** Ship the fail-open provenance/reminder **hook in the v1 install**, or ship the convention **manual-first** and add the hook as a fast follow (its own `hooks/` gate)? *(Changes v1 scope.)*
4. **Backfill.** Adopt the two Backfill Queues (pre-log feedback/decisions from 2026-06-29…2026-07-02) as retroactive entries, or keep both logs **forward-only** from FU.0 / DEC-LLM-001? *(Changes migration scope.)*

---

## Staged Artifacts

All under `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/` — drafts, ready to install post-approval. No framework path touched (P-020).

| File | Purpose | Target |
|------|---------|--------|
| `feedback-decision-logs-standards.md` | MEDIUM rule file draft (LOG-M-001..005 + ≤3 lint) | `.context/rules/` (post-approval) |
| `FEEDBACK-LOG.template.md` | Copy-to-start template with nav + one worked example | `.context/templates/` |
| `LLM-DECISION-LOG.template.md` | Copy-to-start template with nav + boundary banner + example | `.context/templates/` |
| `hook-design-note.md` | Design-only note for the provenance/reminder hook | `hooks/` (separate gate) |

---

## References

`[R]` research = `projects/PROJ-031-cowork-skeleton/research/feedback-decision-log-research.md`; `[B]` bootstrap = `projects/PROJ-031-cowork-skeleton/{FEEDBACK-LOG.md,LLM-DECISION-LOG.md}`; `[G]` governance = `.context/rules/{quality-enforcement.md,markdown-navigation-standards.md}`.

1. `[R] §L0/§L1.A` — [internal-kb] three-log pattern, `R{round}-FU.{n}`, verbatim-wins, DJ-NNN template, `DJ-025` collision, `OI-019`.
2. `[R] §L1.B` — Jerry hooks stdin fields, `DECISION.md` boundary, transcript reality (no native turn), bootstrap files, H-32/H-23/ceiling.
3. `[R] §L2` — automatable-metadata table, DEC-NNN boundary, turn-reference options, install tier constraints.
4. `[B]` — bootstrap schemas (Disposition enum, scoping rule, DEC boundary, Backfill Queues) adopted here.
5. `[G] quality-enforcement.md` — HARD ceiling 25/25 (→ MEDIUM tier), AE-002/AE-003 (→ C3 install gate).
6. `[G] markdown-navigation-standards.md` — H-23 nav table requirement (templates comply).
